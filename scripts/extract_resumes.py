# scripts/extract_resumes.py
import os
import sys
import json
from pathlib import Path

# Add project root to path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parsers.extraction_pipeline import extract_and_save
from utils.logger import get_logger

logger = get_logger(__name__)

INPUT_DIR = "data/raw_resumes"
OUTPUT_DIR = "data/processed_resumes"
SUPPORTED_EXTENSIONS = ('.pdf', '.docx')

def process_all_resumes():
    """Extract and clean text from all resumes in INPUT_DIR using extraction pipeline."""
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

        try:
            # Use the pipeline to extract, clean, and save JSON
            result = extract_and_save(file_path, output_dir=OUTPUT_DIR)
            if result is None:
                logger.error(f"Failed to process {filename}")
                continue

            # The pipeline already saved a JSON file with metadata.
            # We'll also write a separate .txt file with cleaned text for compatibility.
            base_name = os.path.splitext(filename)[0]
            txt_file = os.path.join(OUTPUT_DIR, f"{base_name}.txt")
            with open(txt_file, 'w', encoding='utf-8') as f:
                f.write(result["cleaned_text"])

            logger.info(f"Saved cleaned text to {txt_file} and JSON to {OUTPUT_DIR}/{result['candidate_id']}.json")
        except Exception as e:
            logger.exception(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    process_all_resumes()