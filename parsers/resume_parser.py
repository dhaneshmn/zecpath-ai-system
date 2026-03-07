from utils.logger import get_logger

logger = get_logger(__name__)

def parse_resume(file_path):
    logger.info("Parsing resume")

    extracted_data = {
        "name": "Sample Candidate",
        "skills": ["Python", "Machine Learning"],
        "experience": 3
    }

    return extracted_data