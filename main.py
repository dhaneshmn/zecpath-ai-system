from parsers.resume_parser import parse_resume
from ats_engine.ats_matcher import calculate_ats_score
from screening_ai.screening_model import evaluate_candidate

resume = parse_resume("sample.pdf")

job_skills = ["Python", "Machine Learning", "SQL"]

ats_score = calculate_ats_score(resume["skills"], job_skills)

result = evaluate_candidate(ats_score)

print("ATS Score:", ats_score)
print("Result:", result)