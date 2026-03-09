# tests/test_extraction.py
import os
import sys
import pytest
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parsers.resume_parser import ResumeParser
from parsers.text_cleaner import TextCleaner

SAMPLE_RESUME_DIR = "data/raw_resumes"

@pytest.mark.parametrize("filename", os.listdir(SAMPLE_RESUME_DIR))
def test_extraction(filename):
    """Test that we can extract text from all sample resumes."""
    if not filename.lower().endswith(('.pdf', '.docx')):
        pytest.skip(f"Unsupported file type: {filename}")
    
    file_path = os.path.join(SAMPLE_RESUME_DIR, filename)
    text = ResumeParser.extract_text(file_path)
    assert text is not None, f"Extraction failed for {filename}"
    assert len(text.strip()) > 50, f"Extracted text too short for {filename}"

def test_cleaning():
    """Test cleaning functions on a known string."""
    dirty = "  This  is   a   TEST.   • bullet point  \n\n\n another line."
    clean = TextCleaner.clean(dirty)
    # Check that extra spaces are removed
    assert "  " not in clean
    # Check that bullet is normalized
    assert "•" not in clean
    # Check capitalization
    assert clean.startswith("This")