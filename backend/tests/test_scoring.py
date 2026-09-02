from app.ai.evaluation.final_scorer import calculate_final_score, decide_status


def test_final_score_weighting():
    # 80*0.40 + 70*0.25 + 60*0.20 + 90*0.15 = 32 + 17.5 + 12 + 13.5 = 75.0
    assert calculate_final_score(80, 70, 60, 90) == 75.0


def test_final_score_bounds():
    assert calculate_final_score(100, 100, 100, 100) == 100.0
    assert calculate_final_score(0, 0, 0, 0) == 0.0


def test_shortlist_thresholds():
    assert decide_status(80) == "SHORTLISTED"
    assert decide_status(65) == "REVIEW"
    assert decide_status(30) == "REJECTED"
