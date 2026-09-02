import re

SKILL_ALIASES = {
    "js": "javascript",
    "ts": "typescript",
    "k8s": "kubernetes",
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "rest": "rest api",
    "postgres": "postgresql",
}


class SkillMatcher:
    """Deterministic skill matching layered on top of LLM output."""

    def __init__(self, resume_text: str):
        self.text_lower = resume_text.lower()

    def has_skill(self, skill: str) -> bool:
        normalized = skill.strip().lower()
        candidates = {normalized, SKILL_ALIASES.get(normalized, normalized)}
        # also expand full names back to their abbreviations
        for short, full in SKILL_ALIASES.items():
            if full == normalized:
                candidates.add(short)
        for needle in candidates:
            pattern = r"\b" + re.escape(needle) + r"\b"
            if re.search(pattern, self.text_lower):
                return True
            if needle in self.text_lower:
                return True
        return False
