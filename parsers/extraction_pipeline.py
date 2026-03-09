# parsers/extraction_pipeline.py
import json
from pathlib import Path
from utils.logger import ai_logger
from .pdf_parser import extract_text_from_pdf
from .docx_parser import extract_text_from_docx
from utils.text_cleaner import clean_text

def extract_and_save(file_path: str, output_dir: str = "data/extracted") -> dict:
    """
    Extract text from resume, clean it, and save to output_dir.
    Returns a dict with metadata and cleaned text.
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File {file_path} not found")

    # Determine file type
    suffix = file_path.suffix.lower()
    if suffix == '.pdf':
        raw_text = extract_text_from_pdf(str(file_path))
    elif suffix == '.docx':
        raw_text = extract_text_from_docx(str(file_path))
    else:
        raise ValueError(f"Unsupported file type: {suffix}")

    cleaned_text = clean_text(raw_text)

    # Save cleaned text
    output_path = Path(output_dir) / f"{file_path.stem}.txt"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(cleaned_text)

    # Also save metadata as JSON
    metadata = {
        "original_file": str(file_path),
        "extracted_text_file": str(output_path),
        "length": len(cleaned_text),
        "word_count": len(cleaned_text.split()),
        "status": "success"
    }
    json_path = output_path.with_suffix('.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)

    ai_logger.info(f"Extracted text from {file_path} -> {output_path}")
    return metadata