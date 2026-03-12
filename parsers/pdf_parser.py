# parsers/pdf_parser.py
"""
PDF resume parser with fallback support.
Uses pdfplumber as primary, PyPDF2 as fallback.
"""

import pdfplumber
import PyPDF2
from pathlib import Path
from typing import Union

from utils.logger import get_logger

logger = get_logger(__name__)


def extract_text_from_pdf(pdf_path: Union[str, Path]) -> str:
    """
    Extract text from a PDF file.

    Args:
        pdf_path: Path to the PDF file.

    Returns:
        Extracted text as a single string with pages separated by newlines.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file is not a PDF.
        Exception: If both extraction methods fail.
    """
    pdf_path = Path(pdf_path)

    # Validate file
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    if pdf_path.suffix.lower() != '.pdf':
        raise ValueError(f"File is not a PDF: {pdf_path}")

    full_text = []

    # Try pdfplumber first (better layout preservation)
    try:
        logger.info(f"Extracting text from {pdf_path} using pdfplumber")
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                # Use layout=True to better handle columns and tables
                page_text = page.extract_text(layout=True)
                if page_text:
                    full_text.append(page_text)
                else:
                    logger.warning(f"No text found on page {page_num} in {pdf_path}")
        logger.info(f"Successfully extracted {len(full_text)} pages with pdfplumber")

    except Exception as e:
        logger.warning(f"pdfplumber failed for {pdf_path}, falling back to PyPDF2: {e}")
        full_text = []  # Reset in case partial extraction occurred

        # Fallback to PyPDF2
        try:
            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page_num, page in enumerate(reader.pages, start=1):
                    page_text = page.extract_text()
                    if page_text:
                        full_text.append(page_text)
                    else:
                        logger.warning(f"No text found on page {page_num} in {pdf_path} (PyPDF2)")
            logger.info(f"Successfully extracted {len(full_text)} pages with PyPDF2")

        except Exception as e2:
            logger.error(f"Both pdfplumber and PyPDF2 failed for {pdf_path}: {e2}")
            raise

    return "\n".join(full_text)