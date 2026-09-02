from app.ai.evaluation.evaluation_schemas import SCORE_WEIGHTS


def calculate_final_score(
    skill_score: int, experience_score: int, semantic_score: int, ats_score: int
) -> float:
    """Weighted final score. All inputs 0-100; weights centralized here.

    Skill Match      40%
    Experience       25%
    Semantic Match   20%
    ATS Quality      15%
    """
    weighted = (
        skill_score * SCORE_WEIGHTS["skill"]
        + experience_score * SCORE_WEIGHTS["experience"]
        + semantic_score * SCORE_WEIGHTS["semantic"]
        + ats_score * SCORE_WEIGHTS["ats"]
    )
    return round(min(max(weighted, 0.0), 100.0), 1)


def decide_status(final_score: float, shortlist_threshold: int = 75, review_threshold: int = 60) -> str:
    if final_score >= shortlist_threshold:
        return "SHORTLISTED"
    if final_score >= review_threshold:
        return "REVIEW"
    return "REJECTED"
