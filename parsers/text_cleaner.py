# parsers/text_cleaner.py
"""
Text cleaning and normalization utilities for resume parsing.
"""

import re
import unicodedata
from typing import List, Optional

from utils.logger import get_logger

logger = get_logger(__name__)


class TextCleaner:
    """Clean and normalize extracted resume text."""

    @staticmethod
    def normalize_unicode(text: str) -> str:
        """Normalize unicode characters (e.g., smart quotes to ASCII)."""
        return unicodedata.normalize('NFKD', text)

    @staticmethod
    def normalize_whitespace(text: str) -> str:
        """Replace multiple spaces/tabs with single space, and normalize newlines."""
        # Replace tabs and multiple spaces
        text = re.sub(r'[ \t]+', ' ', text)
        # Replace multiple newlines with a single newline (but keep paragraph breaks)
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()

    @staticmethod
    def normalize_bullets(text: str) -> str:
        """Convert various bullet symbols to a standard '-'."""
        # Common bullet unicode characters and symbols
        bullet_pattern = r'[•●▪➢➤→∙⁃·‣⁌⁍]'
        text = re.sub(bullet_pattern, '-', text)
        return text

    @staticmethod
    def remove_control_characters(text: str) -> str:
        """Remove control characters except newline and tab."""
        return ''.join(char for char in text if ord(char) >= 32 or char in '\n\t')

    @classmethod
    def clean(cls, text: str, apply_capitalization: bool = False) -> str:
        """
        Apply all cleaning steps.

        Args:
            text: Raw extracted text.
            apply_capitalization: If True, attempt to fix sentence capitalization (not recommended for resumes).

        Returns:
            Cleaned text.
        """
        if not text:
            return ""

        original_len = len(text)
        text = cls.normalize_unicode(text)
        text = cls.remove_control_characters(text)
        text = cls.normalize_whitespace(text)
        text = cls.normalize_bullets(text)

        # Optionally, apply capitalization (disabled by default)
        if apply_capitalization:
            text = cls.fix_capitalization(text)

        logger.debug(f"Cleaned text: {original_len} chars -> {len(text)} chars")
        return text

    @staticmethod
    def fix_capitalization(text: str) -> str:
        """
        Basic sentence capitalization (use with caution).
        May break proper nouns.
        """
        sentences = re.split(r'(?<=[.!?])\s+', text)
        capitalized = []
        for s in sentences:
            if s and s[0].islower():
                s = s[0].upper() + s[1:]
            capitalized.append(s)
        return ' '.join(capitalized)