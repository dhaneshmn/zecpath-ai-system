# parsers/jd_parser.py
"""
Job Description Parser – converts raw job posting text into structured AI‑ready objects.
Uses the same skill configuration and text cleaning as the resume pipeline.
"""

import re
import json
from pathlib import Path
from typing import Optional, Dict, Any, List, Union

from parsers.text_cleaner import TextCleaner
from utils.logger import get_logger

logger = get_logger(__name__)

# Load skill configuration (shared with resume skill extraction)
CONFIG_PATH = Path("config/skills.json")
if CONFIG_PATH.exists():
    with open(CONFIG_PATH) as f:
        SKILL_CONFIG = json.load(f)
    SKILL_LIST = [s.lower() for s in SKILL_CONFIG.get("skills", [])]
    SYNONYM_MAP = {k.lower(): v.lower() for k, v in SKILL_CONFIG.get("synonyms", {}).items()}
else:
    logger.warning("config/skills.json not found. Using empty skill lists.")
    SKILL_LIST = []
    SYNONYM_MAP = {}


class JobDescriptionParser:
    """
    Parser for job descriptions. Extracts structured information from raw text.
    """

    def __init__(self, text: str):
        """
        Initialize with raw job description text.
        """
        self.raw_text = text
        self.cleaned_text = TextCleaner.clean(text)
        self.lines = self.cleaned_text.splitlines()

    def parse(self) -> Dict[str, Any]:
        """
        Main entry point: returns a structured job profile.
        """
        return {
            "job_id": None,  # To be assigned by the caller (e.g., from filename)
            "company": self._extract_company(),
            "title": self._extract_title(),
            "location": self._extract_location(),
            "employment_type": self._extract_employment_type(),
            "experience_required": self._extract_experience(),
            "education_required": self._extract_education(),
            "skills_required": self._extract_skills_with_importance(),
            "responsibilities": self._extract_responsibilities(),
            "benefits": self._extract_benefits(),
            "salary_range": self._extract_salary(),
            "posted_date": self._extract_posted_date(),
            "application_deadline": self._extract_deadline(),
            "raw_text": self.raw_text,
            "cleaned_text": self.cleaned_text,
        }

    # ----------------------------------------------------------------------
    # Individual extraction methods (can be overridden or extended)
    # ----------------------------------------------------------------------

    def _extract_company(self) -> Optional[str]:
        patterns = [
            r"(?:company|organization|employer)\s*[:\-]?\s*(.+)",
            r"^(.+?)(?:\||\-|job description|hiring)",
        ]
        for pattern in patterns:
            match = re.search(pattern, self.cleaned_text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        for line in self.lines:
            line = line.strip()
            if line and len(line) < 50 and not line.isupper():
                return line
        return None

    def _extract_title(self) -> Optional[str]:
        patterns = [
            r"job\s*title\s*[:\-]?\s*(.+)",
            r"role\s*[:\-]?\s*(.+)",
            r"position\s*[:\-]?\s*(.+)",
            r"^(.+developer|engineer|analyst|manager|designer|specialist|consultant).*$",
        ]
        for pattern in patterns:
            match = re.search(pattern, self.cleaned_text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        for line in self.lines:
            if line.strip():
                return line.strip()
        return None

    def _extract_location(self) -> Dict[str, Any]:
        location = {"city": None, "state": None, "country": None, "remote": False}
        text_lower = self.cleaned_text.lower()
        if re.search(r"\b(remote|work from home|virtual)\b", text_lower):
            location["remote"] = True
        patterns = [
            r"location\s*[:\-]?\s*([^,\n]+)[,\s]+([A-Z]{2})",
            r"location\s*[:\-]?\s*([^,\n]+)",
        ]
        for pattern in patterns:
            match = re.search(pattern, self.cleaned_text, re.IGNORECASE)
            if match:
                groups = match.groups()
                if len(groups) >= 2:
                    location["city"] = groups[0].strip()
                    location["state"] = groups[1].strip()
                elif len(groups) == 1:
                    location["city"] = groups[0].strip()
                break
        return location

    def _extract_employment_type(self) -> Optional[str]:
        text_lower = self.cleaned_text.lower()
        types = ["full-time", "part-time", "contract", "internship", "temporary", "freelance"]
        for t in types:
            if t in text_lower:
                return t
        if "ft" in text_lower or "full time" in text_lower:
            return "full-time"
        if "pt" in text_lower or "part time" in text_lower:
            return "part-time"
        return None

    def _extract_experience(self) -> Dict[str, Any]:
        text_lower = self.cleaned_text.lower()
        years = []
        patterns = [
            r"(\d+)\s*[\-\+]\s*years?",
            r"(\d+)\s*years?",
            r"minimum\s*(\d+)\s*years?",
            r"at\s*least\s*(\d+)\s*years?",
        ]
        for pattern in patterns:
            matches = re.findall(pattern, text_lower)
            years.extend([int(m) for m in matches])
        if years:
            min_exp = min(years)
            max_exp = max(years)
        else:
            min_exp = max_exp = None
        exp_sentences = re.findall(r"[^.]*?years?[^.]*\.", text_lower)
        description = exp_sentences[0] if exp_sentences else ""
        return {
            "minimum_years": min_exp,
            "maximum_years": max_exp,
            "description": description,
        }

    def _extract_education(self) -> List[Dict[str, Any]]:
        text_lower = self.cleaned_text.lower()
        degree_map = {
            "bachelor": "Bachelor's",
            "b.s.": "Bachelor's",
            "b.a.": "Bachelor's",
            "master": "Master's",
            "m.s.": "Master's",
            "mba": "MBA",
            "phd": "PhD",
            "doctorate": "PhD",
            "high school": "High School",
            "associate": "Associate's",
        }
        fields = ["computer science", "engineering", "business", "marketing", "finance",
                  "information technology", "data science", "mathematics", "statistics"]
        found = []
        for deg_key, deg_name in degree_map.items():
            if deg_key in text_lower:
                field = None
                for f in fields:
                    if f in text_lower:
                        field = f
                        break
                found.append({
                    "degree": deg_name,
                    "field": field,
                    "is_mandatory": True,
                })
        return found

    def _extract_skills_with_importance(self) -> List[Dict[str, Any]]:
        sentences = re.split(r'(?<=[.!?])\s+', self.cleaned_text.lower())
        found = set()
        for synonym, canonical in SYNONYM_MAP.items():
            if synonym in self.cleaned_text.lower():
                found.add(canonical)
        for skill in SKILL_LIST:
            if skill in self.cleaned_text.lower():
                found.add(skill)
        skills_with_importance = []
        for skill in found:
            importance = "must-have"
            for sent in sentences:
                if skill in sent:
                    if re.search(r'(preferred|nice to have|plus)', sent):
                        importance = "nice-to-have"
                        break
            skills_with_importance.append({
                "name": skill,
                "importance": importance,
            })
        return skills_with_importance

    def _extract_responsibilities(self) -> List[str]:
        lines = self.lines
        responsibilities = []
        in_section = False
        section_headers = ["responsibilities", "what you'll do", "duties", "role overview"]
        for line in lines:
            line_lower = line.lower().strip()
            if any(header in line_lower for header in section_headers):
                in_section = True
                continue
            if in_section:
                if re.match(r"^[a-z\s]{3,}:$", line_lower) or line_lower in ["qualifications", "requirements", "benefits"]:
                    break
                if line.strip() and (line.startswith(('•', '-', '·')) or re.match(r'^\d+\.', line)):
                    responsibilities.append(line.lstrip('•-·0123456789. ').strip())
                elif line.strip() and len(line) > 20:
                    responsibilities.append(line.strip())
        return responsibilities

    def _extract_benefits(self) -> List[str]:
        lines = self.lines
        benefits = []
        in_section = False
        section_headers = ["benefits", "perks", "what we offer", "compensation"]
        for line in lines:
            line_lower = line.lower().strip()
            if any(header in line_lower for header in section_headers):
                in_section = True
                continue
            if in_section:
                if re.match(r"^[a-z\s]{3,}:$", line_lower) or line_lower in ["qualifications", "requirements"]:
                    break
                if line.strip() and (line.startswith(('•', '-', '·')) or re.match(r'^\d+\.', line)):
                    benefits.append(line.lstrip('•-·0123456789. ').strip())
        return benefits

    def _extract_salary(self) -> Optional[Dict[str, Any]]:
        text = self.cleaned_text
        salary_patterns = [
            r"\$(\d{1,3}(?:,\d{3})?)\s*[-–]\s*\$(\d{1,3}(?:,\d{3})?)\s*(per|/)?\s*(year|annum|month|hour)",
            r"\$(\d{1,3}(?:,\d{3})?)\s*(per|/)?\s*(year|annum|month|hour)",
        ]
        for pattern in salary_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                groups = match.groups()
                if len(groups) >= 4 and groups[1] is not None:
                    min_sal = int(groups[0].replace(',', ''))
                    max_sal = int(groups[1].replace(',', ''))
                    period = groups[3] if groups[3] else "year"
                elif len(groups) >= 3:
                    min_sal = int(groups[0].replace(',', ''))
                    max_sal = None
                    period = groups[2] if groups[2] else "year"
                else:
                    continue
                period_map = {"year": "yearly", "annum": "yearly", "month": "monthly", "hour": "hourly"}
                period = period_map.get(period.lower(), "yearly")
                return {
                    "min": min_sal,
                    "max": max_sal,
                    "currency": "USD",
                    "period": period,
                }
        return None

    def _extract_posted_date(self) -> Optional[str]:
        patterns = [
            r"posted\s*[:\-]?\s*(\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4})",
            r"date posted\s*[:\-]?\s*(\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4})",
        ]
        for pattern in patterns:
            match = re.search(pattern, self.cleaned_text, re.IGNORECASE)
            if match:
                return match.group(1)
        return None

    def _extract_deadline(self) -> Optional[str]:
        patterns = [
            r"deadline\s*[:\-]?\s*(\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4})",
            r"apply by\s*[:\-]?\s*(\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4})",
        ]
        for pattern in patterns:
            match = re.search(pattern, self.cleaned_text, re.IGNORECASE)
            if match:
                return match.group(1)
        return None


# ----------------------------------------------------------------------
# Convenience function for one‑off parsing
# ----------------------------------------------------------------------
def parse_job_description(text: str) -> Dict[str, Any]:
    parser = JobDescriptionParser(text)
    return parser.parse()


def parse_jd_file(file_path: Union[str, Path]) -> Dict[str, Any]:
    file_path = Path(file_path)
    if file_path.suffix.lower() in ('.pdf', '.docx'):
        from parsers.extraction_pipeline import extract_raw_text
        text = extract_raw_text(file_path)
        if text is None:
            raise ValueError(f"Could not extract text from {file_path}")
    else:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    return parse_job_description(text)


# ----------------------------------------------------------------------
# Batch processing
# ----------------------------------------------------------------------
def process_jd_batch(input_dir: Union[str, Path], output_dir: Union[str, Path]) -> List[Path]:
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    supported = ['.txt', '.pdf', '.docx']
    files = []
    for ext in supported:
        files.extend(input_dir.glob(f"*{ext}"))
    saved = []
    for file_path in files:
        try:
            jd_data = parse_jd_file(file_path)
            job_id = file_path.stem
            jd_data["job_id"] = job_id
            out_path = output_dir / f"{job_id}.json"
            with open(out_path, 'w', encoding='utf-8') as f:
                json.dump(jd_data, f, indent=2, ensure_ascii=False)
            saved.append(out_path)
            logger.info(f"Saved {out_path}")
        except Exception as e:
            logger.error(f"Failed to process {file_path}: {e}")
    return saved