from ats_engine.ats_matcher import calculate_ats_score

def test_ats_score():

    candidate = ["Python", "SQL"]
    job = ["Python", "SQL", "ML"]

    score = calculate_ats_score(candidate, job)

    assert score > 0