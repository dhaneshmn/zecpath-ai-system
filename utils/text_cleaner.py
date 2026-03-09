# utils/text_cleaner.py
import re
import unicodedata

def normalize_unicode(text: str) -> str:
    """Convert to NFKC form to handle special characters."""
    return unicodedata.normalize('NFKC', text)

def remove_extra_whitespace(text: str) -> str:
    """Replace multiple spaces/newlines with single space, but keep paragraph breaks? We'll keep double newlines for sections."""
    # Replace multiple newlines with a single newline, but keep at most two for paragraph separation.
    text = re.sub(r'\n\s*\n', '\n\n', text)
    # Replace multiple spaces with a single space.
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()

def normalize_bullets(text: str) -> str:
    """Replace bullet characters with a standard marker."""
    bullet_pattern = r'[•●▪■➢➤→]'
    text = re.sub(bullet_pattern, '-', text)
    return text

def clean_text(raw_text: str) -> str:
    """Apply all cleaning steps."""
    text = normalize_unicode(raw_text)
    text = normalize_bullets(text)
    text = remove_extra_whitespace(text)
    # You could add more: fix hyphenation, etc.
    return text