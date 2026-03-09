# parsers/docx_parser.py
from docx import Document
from pathlib import Path
from utils.logger import ai_logger

def extract_text_from_docx(docx_path: str) -> str:
    """
    Extract text from a DOCX file using python-docx.
    Concatenates all paragraphs.
    """
    try:
        doc = Document(docx_path)
        full_text = [para.text for para in doc.paragraphs if para.text.strip()]
        # Also extract text from tables?
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    cell_text = cell.text.strip()
                    if cell_text:
                        full_text.append(cell_text)
        return "\n".join(full_text)
    except Exception as e:
        ai_logger.error(f"Failed to extract text from {docx_path}: {e}")
        raise