from utils.logger import get_logger

logger = get_logger(__name__)

def evaluate_candidate(score):

    logger.info("Evaluating candidate")

    if score > 70:
        return "Shortlisted"
    else:
        return "Rejected"