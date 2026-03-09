# tests/test_extractors.py
import pytest
from pathlib import Path
from parsers.extraction_pipeline import extract_and_save
from parsers.pdf_parser import extract_text_from_pdf
from parsers.docx_parser import extract_text_from_docx

SAMPLE_DIR = Path("data/sample_resumes")

def test_pdf_extraction():
    pdf_files = list(SAMPLE_DIR.glob("*.pdf"))
    assert len(pdf_files) > 0, "No PDF sample files found"
    for pdf_file in pdf_files:
        text = extract_text_from_pdf(str(pdf_file))
        assert text, f"Extracted text empty for {pdf_file}"
        assert len(text) > 50, f"Text too short for {pdf_file}"

def test_docx_extraction():
    docx_files = list(SAMPLE_DIR.glob("*.docx"))
    assert len(docx_files) > 0, "No DOCX sample files found"
    for docx_file in docx_files:
        text = extract_text_from_docx(str(docx_file))
        assert text, f"Extracted text empty for {docx_file}"
        assert len(text) > 50, f"Text too short for {docx_file}"

def test_extraction_pipeline():
    pdf_files = list(SAMPLE_DIR.glob("*.pdf"))
    if pdf_files:
        metadata = extract_and_save(str(pdf_files[0]), output_dir="data/test_output")
        assert metadata["status"] == "success"
        assert Path(metadata["extracted_text_file"]).exists()