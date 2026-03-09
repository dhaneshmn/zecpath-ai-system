# parsers/resume_parser.py
import os
import pdfplumber
import PyPDF2
from docx import Document
from typing import Optional
import logging
from utils.logger import get_logger

logger = get_logger(__name__)

class ResumeParser:
    """Extract text from resume files (PDF, DOCX)."""

    @staticmethod
    def extract_text_from_pdf(file_path: str) -> Optional[str]:
        """Extract text from a PDF file using pdfplumber (fallback to PyPDF2)."""
        text = ""
        try:
            # Try pdfplumber first (better for complex layouts)
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            if text.strip():
                logger.info(f"Successfully extracted text from {file_path} using pdfplumber")
                return text
        except Exception as e:
            logger.warning(f"pdfplumber failed for {file_path}: {e}. Trying PyPDF2...")

        # Fallback to PyPDF2
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            if text.strip():
                logger.info(f"Successfully extracted text from {file_path} using PyPDF2")
                return text
            else:
                logger.error(f"No text extracted from {file_path} using either method")
                return None
        except Exception as e:
            logger.error(f"Failed to extract text from {file_path} with PyPDF2: {e}")
            return None

    @staticmethod
    def extract_text_from_docx(file_path: str) -> Optional[str]:
        """Extract text from a DOCX file."""
        try:
            doc = Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
            if text.strip():
                logger.info(f"Successfully extracted text from {file_path}")
                return text
            else:
                logger.error(f"No text found in {file_path}")
                return None
        except Exception as e:
            logger.error(f"Failed to extract text from {file_path}: {e}")
            return None

    @classmethod
    def extract_text(cls, file_path: str) -> Optional[str]:
        """Main entry point: extract text based on file extension."""
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return None

        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.pdf':
            return cls.extract_text_from_pdf(file_path)
        elif ext == '.docx':
            return cls.extract_text_from_docx(file_path)
        else:
            logger.error(f"Unsupported file type: {ext}")
            return None