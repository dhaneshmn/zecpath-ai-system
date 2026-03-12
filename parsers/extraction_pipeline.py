# parsers/extraction_pipeline.py
"""
Complete resume extraction pipeline with batch processing.
Extracts text from PDF/DOCX, cleans it, and saves as:
- JSON file containing raw text, cleaned text, metadata, and a unique candidate ID.
- .txt file containing only the cleaned text (for backward compatibility).
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Union, List, Optional

# Import specialized parsers
from .pdf_parser import extract_text_from_pdf
from .docx_parser import extract_text_from_docx

# Import text cleaner (adjust import based on your actual location)
try:
    from utils.text_cleaner import clean_text
except ImportError:
    from .text_cleaner import TextCleaner
    clean_text = TextCleaner.clean

from utils.logger import get_logger

logger = get_logger(__name__)


def extract_raw_text(file_path: Union[str, Path]) -> Optional[str]:
    """
    Extract raw text from a file without cleaning or saving.
    Useful for testing and one‑off uses.
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    ext = file_path.suffix.lower()
    if ext == '.pdf':
        return extract_text_from_pdf(file_path)
    elif ext == '.docx':
        return extract_text_from_docx(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")


def extract_and_save(
    file_path: Union[str, Path],
    output_dir: Union[str, Path] = "data/processed_resumes",
    candidate_id: Optional[str] = None
) -> dict:
    """
    Extract text from a single resume, clean it, and save as JSON and .txt.

    Args:
        file_path: Path to the resume file (PDF or DOCX).
        output_dir: Directory where output files will be saved.
        candidate_id: Optional custom candidate ID. If not provided, one is generated.

    Returns:
        Dictionary containing metadata, including paths to saved files and a 'status' field.

    Raises:
        FileNotFoundError: If file does not exist.
        ValueError: If file type is unsupported.
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    # Determine file type and extract raw text
    suffix = file_path.suffix.lower()
    if suffix == '.pdf':
        raw_text = extract_text_from_pdf(file_path)
        parser_used = 'pdf_parser'
    elif suffix == '.docx':
        raw_text = extract_text_from_docx(file_path)
        parser_used = 'docx_parser'
    else:
        raise ValueError(f"Unsupported file type: {suffix}")

    if not raw_text:
        logger.error(f"No text extracted from {file_path}")
        return None

    # Clean text
    cleaned_text = clean_text(raw_text)

    # Generate candidate ID if not provided
    if candidate_id is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        candidate_id = f"{file_path.stem}_{timestamp}"

    # Prepare output directory
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save JSON
    json_path = output_dir / f"{candidate_id}.json"
    output_data = {
        "candidate_id": candidate_id,
        "file_name": file_path.name,
        "raw_text": raw_text,
        "cleaned_text": cleaned_text,
        "extraction_metadata": {
            "parser": parser_used,
            "extracted_at": datetime.now().isoformat(),
            "original_file": str(file_path)
        },
        "status": "success"
    }
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    # Save cleaned text as .txt for compatibility (as expected by tests and extract_resumes.py)
    txt_path = output_dir / f"{candidate_id}.txt"
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(cleaned_text)

    # Add the .txt file path to the returned metadata
    output_data["extracted_text_file"] = str(txt_path)

    logger.info(f"Saved extracted resume to {json_path} and {txt_path}")
    return output_data


def process_batch(
    input_dir: Union[str, Path] = "data/raw_resumes",
    output_dir: Union[str, Path] = "data/processed_resumes",
    file_patterns: List[str] = None
) -> List[dict]:
    """
    Process all resume files in a directory.

    Args:
        input_dir: Directory containing raw resume files.
        output_dir: Directory where processed files will be saved.
        file_patterns: List of glob patterns to match (default: ['*.pdf', '*.docx']).

    Returns:
        List of result dictionaries for successfully processed files.
    """
    input_dir = Path(input_dir)
    if not input_dir.exists():
        logger.error(f"Input directory does not exist: {input_dir}")
        return []

    if file_patterns is None:
        file_patterns = ['*.pdf', '*.docx']

    files = []
    for pattern in file_patterns:
        files.extend(input_dir.glob(pattern))

    if not files:
        logger.warning(f"No matching files found in {input_dir}")
        return []

    results = []
    for file_path in files:
        try:
            result = extract_and_save(file_path, output_dir)
            if result:
                results.append(result)
        except Exception as e:
            logger.exception(f"Failed to process {file_path}: {e}")

    logger.info(f"Batch processing complete. Processed {len(results)}/{len(files)} files.")
    return results


# If this script is run directly, process all files in default raw directory
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        result = extract_and_save(sys.argv[1])
        print(f"Processed: {result['candidate_id'] if result else 'Failed'}")
    else:
        process_batch()