import pytest
from parsers.jd_parser import parse_job_description

def test_title_extraction():
    text = "Job Title: Senior Python Developer"
    jd = parse_job_description(text)
    assert jd["title"] == "Senior Python Developer"

def test_skill_extraction():
    text = "Required: Python, Django. Preferred: AWS."
    jd = parse_job_description(text)
    skills = {s["name"]: s["importance"] for s in jd["skills_required"]}
    assert skills["python"] == "must-have"
    assert skills["django"] == "must-have"
    assert skills["aws"] == "nice-to-have"