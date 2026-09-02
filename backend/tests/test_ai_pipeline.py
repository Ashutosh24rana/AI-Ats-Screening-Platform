from app.ai.evaluation.skill_matcher import SkillMatcher


def test_skill_matcher_positive():
    matcher = SkillMatcher("Skilled in Python and FastAPI, built REST APIs with PostgreSQL.")
    assert matcher.has_skill("Python")
    assert matcher.has_skill("FastAPI")


def test_skill_matcher_negative():
    matcher = SkillMatcher("Experienced with React and TypeScript.")
    assert not matcher.has_skill("Kubernetes")


def test_skill_alias_matching():
    matcher = SkillMatcher("5 years of JS experience.")
    assert matcher.has_skill("javascript") or matcher.has_skill("JS")
