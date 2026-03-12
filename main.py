# main.py
import json
from pathlib import Path

from parsers.extraction_pipeline import extract_and_save
from ats_engine.ats_matcher import calculate_ats_score
from screening_ai.screening_model import evaluate_candidate
from utils.logger import get_logger

logger = get_logger(__name__)

# Load skill configuration (same as used in jd_parser)
with open("config/skills.json") as f:
    SKILL_CONFIG = json.load(f)
SKILL_LIST = [s.lower() for s in SKILL_CONFIG["skills"]]
SYNONYM_MAP = {k.lower(): v.lower() for k, v in SKILL_CONFIG["synonyms"].items()}

def extract_skills_from_text(text: str) -> list:
    """Simple keyword-based skill extraction from cleaned resume text."""
    text_lower = text.lower()
    found = set()

    # Apply synonym mapping
    for synonym, canonical in SYNONYM_MAP.items():
        if synonym in text_lower:
            found.add(canonical)

    # Look for canonical skill names
    for skill in SKILL_LIST:
        if skill in text_lower:
            found.add(skill)

    return list(found)

def find_sample_file() -> Path:
    """Return the first PDF or DOCX file in data/sample_resumes/."""
    sample_dir = Path("data/sample_resumes")
    if not sample_dir.exists():
        raise FileNotFoundError(f"Sample directory {sample_dir} not found.")
    pdfs = list(sample_dir.glob("*.pdf"))
    docxs = list(sample_dir.glob("*.docx"))
    all_files = pdfs + docxs
    if not all_files:
        raise FileNotFoundError(f"No sample PDF/DOCX files found in {sample_dir}.")
    return all_files[0]

def main():
    try:
        sample_file = find_sample_file()
        logger.info(f"Using sample file: {sample_file}")
    except FileNotFoundError as e:
        logger.error(e)
        return

    # Use the extraction pipeline to process the resume
    result = extract_and_save(sample_file, output_dir="data/processed_resumes")
    if not result:
        logger.error("Failed to extract resume")
        return

    cleaned_text = result["cleaned_text"]
    candidate_id = result["candidate_id"]

    # Extract skills from cleaned text (temporary until Day 6)
    extracted_skills = extract_skills_from_text(cleaned_text)
    logger.info(f"Extracted skills: {extracted_skills}")

    # Job skills (example)
    job_skills = ["Python", "Machine Learning", "SQL"]

    # Calculate ATS score (placeholder – ats_matcher may need updating)
    ats_score = calculate_ats_score(extracted_skills, job_skills)

    # Screening evaluation (placeholder)
    eval_result = evaluate_candidate(ats_score)

    print(f"Candidate ID: {candidate_id}")
    print(f"ATS Score: {ats_score}")
    print(f"Result: {eval_result}")

if __name__ == "__main__":
    main()