# scripts/extract_resumes.py
import os
import sys
import json
from pathlib import Path

# Add project root to path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parsers.resume_parser import ResumeParser
from parsers.text_cleaner import TextCleaner
from utils.logger import get_logger

logger = get_logger(__name__)

INPUT_DIR = "data/raw_resumes"
OUTPUT_DIR = "data/processed_resumes"
SUPPORTED_EXTENSIONS = ('.pdf', '.docx')

def process_all_resumes():
    """Extract and clean text from all resumes in INPUT_DIR."""
    if not os.path.exists(INPUT_DIR):
        logger.error(f"Input directory {INPUT_DIR} does not exist.")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    resume_files = [f for f in os.listdir(INPUT_DIR) 
                    if f.lower().endswith(SUPPORTED_EXTENSIONS)]
    
    if not resume_files:
        logger.warning(f"No resume files found in {INPUT_DIR}")
        return

    for filename in resume_files:
        file_path = os.path.join(INPUT_DIR, filename)
        logger.info(f"Processing {filename}...")

        # Extract raw text
        raw_text = ResumeParser.extract_text(file_path)
        if raw_text is None:
            logger.error(f"Failed to extract text from {filename}")
            continue

        # Clean text
        cleaned_text = TextCleaner.clean(raw_text)

        # Save output
        base_name = os.path.splitext(filename)[0]
        output_file = os.path.join(OUTPUT_DIR, f"{base_name}.txt")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(cleaned_text)

        # Also save as JSON with metadata (optional)
        metadata = {
            "original_file": filename,
            "extracted_text": cleaned_text,
            "character_count": len(cleaned_text)
        }
        json_output = os.path.join(OUTPUT_DIR, f"{base_name}.json")
        with open(json_output, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)

        logger.info(f"Saved cleaned text to {output_file} and {json_output}")

if __name__ == "__main__":
    process_all_resumes()