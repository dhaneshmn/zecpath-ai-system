# parsers/jd_parser.py
import os
import re
import json
from typing import Optional, Dict, Any, List
from parsers.resume_parser import ResumeParser
from parsers.text_cleaner import TextCleaner
from utils.logger import get_logger

logger = get_logger(__name__)