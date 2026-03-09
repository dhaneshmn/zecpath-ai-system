# parsers/pdf_parser.py
import pdfplumber
from pathlib import Path
from utils.logger import ai_logger

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from a PDF file using pdfplumber.
    Handles multiple pages and attempts to preserve layout.
    """
    full_text = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                # Extract text from page; you can also try .extract_text(layout=True) for better layout
                page_text = page.extract_text()
                if page_text:
                    full_text.append(page_text)
                else:
                    # Fallback: maybe extract text from tables or use OCR? (not now)
                    ai_logger.warning(f"No text found on page {page.page_number} in {pdf_path}")
        return "\n".join(full_text)
    except Exception as e:
        ai_logger.error(f"Failed to extract text from {pdf_path}: {e}")
        raise