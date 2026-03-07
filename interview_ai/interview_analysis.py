from utils.logger import get_logger

logger = get_logger(__name__)

def analyze_interview(transcript):

    logger.info("Analyzing interview")

    result = {
        "confidence_score": 80,
        "communication_score": 75,
        "technical_score": 85
    }

    return result