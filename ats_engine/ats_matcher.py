from utils.logger import get_logger

logger = get_logger(__name__)

def calculate_ats_score(candidate_skills, job_skills):

    logger.info("Calculating ATS Score")

    matched = set(candidate_skills).intersection(set(job_skills))

    score = len(matched) / len(job_skills) * 100

    return score