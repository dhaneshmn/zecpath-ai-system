# parsers/text_cleaner.py
import re
from typing import List

class TextCleaner:
    """Clean and normalize extracted resume text."""

    @staticmethod
    def normalize_whitespace(text: str) -> str:
        """Replace multiple spaces/tabs/newlines with single spaces."""
        # Replace tabs and multiple spaces
        text = re.sub(r'[ \t]+', ' ', text)
        # Replace multiple newlines with a single newline
        text = re.sub(r'\n\s*\n', '\n\n', text)
        return text.strip()

    @staticmethod
    def normalize_bullets(text: str) -> str:
        """Convert various bullet symbols to a standard '-'."""
        # Common bullet unicode characters and symbols
        bullet_pattern = r'[•●▪➢➤→∙⁃·‣⁌⁍]'
        text = re.sub(bullet_pattern, '-', text)
        return text

    @staticmethod
    def fix_capitalization(text: str) -> str:
        """Ensure proper sentence capitalization (basic)."""
        # Simple: capitalize first letter after period + space
        sentences = re.split(r'(?<=[.!?])\s+', text)
        capitalized = []
        for s in sentences:
            if s:
                s = s[0].upper() + s[1:] if s[0].islower() else s
            capitalized.append(s)
        return ' '.join(capitalized)

    @staticmethod
    def remove_noise(text: str) -> str:
        """Remove stray characters and noise."""
        # Remove control characters except newline
        text = ''.join(char for char in text if ord(char) >= 32 or char == '\n')
        # Optionally remove email/phone patterns if they cause issues (we may want to keep them)
        # For now, keep everything.
        return text

    @classmethod
    def clean(cls, text: str) -> str:
        """Apply all cleaning steps."""
        if not text:
            return ""
        text = cls.remove_noise(text)
        text = cls.normalize_whitespace(text)
        text = cls.normalize_bullets(text)
        text = cls.fix_capitalization(text)
        return text