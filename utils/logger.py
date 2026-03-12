import logging
import logging.handlers
import sys
import os   # <-- add this line
from pathlib import Path
import json
from typing import Optional

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

def setup_logger(
    name: str,
    log_file: str = "ai_activities.log",
    level: Optional[int] = None,
    enable_console: bool = True,
    enable_json: bool = False
) -> logging.Logger:
    """
    Configure and return a logger with file (rotating) and optional console handlers.
    
    Args:
        name: Logger name.
        log_file: Base name for log file (will be placed in LOG_DIR).
        level: Logging level (defaults to INFO, can be overridden by env var).
        enable_console: Whether to add console handler.
        enable_json: If True, also create a JSON lines log file for structured data.
    """
    if level is None:
        level = getattr(logging, os.getenv("LOG_LEVEL", "INFO"))

    logger = logging.getLogger(name)
    
    # Prevent adding duplicate handlers
    if logger.handlers:
        return logger

    logger.setLevel(level)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Rotating file handler (10 MB per file, keep 5 backups)
    file_handler = logging.handlers.RotatingFileHandler(
        LOG_DIR / log_file, maxBytes=10_485_760, backupCount=5
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Separate error file handler
    error_handler = logging.handlers.RotatingFileHandler(
        LOG_DIR / "errors.log", maxBytes=10_485_760, backupCount=5
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    logger.addHandler(error_handler)

    if enable_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    if enable_json:
        # JSON handler for structured logs (e.g., decisions)
        json_handler = logging.handlers.RotatingFileHandler(
            LOG_DIR / "decisions.json", maxBytes=10_485_760, backupCount=5
        )
        json_handler.setLevel(logging.INFO)
        # Use a custom formatter that outputs JSON
        json_handler.setFormatter(JsonFormatter())
        logger.addHandler(json_handler)

    return logger

class JsonFormatter(logging.Formatter):
    """Custom formatter to output logs as JSON lines."""
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "name": record.name,
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        # Add extra fields if present (e.g., decision_id)
        if hasattr(record, 'decision_id'):
            log_record['decision_id'] = record.decision_id
        return json.dumps(log_record)

# Factory function
def get_logger(name: str, **kwargs) -> logging.Logger:
    """Convenience function to get a configured logger."""
    return setup_logger(name, **kwargs)

# Example usage in a module:
# logger = get_logger(__name__)
# logger.info("Normal log")
# logger.error("Error log")
# logger.warning("Warning", extra={'decision_id': '123'})  # For JSON