from pydantic import BaseModel, Field, field_validator


class SkillEvaluation(BaseModel):
    """Structured LLM output for skill matching."""

    matched_skills: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)
    skill_score: int = Field(ge=0, le=100)


class ExperienceEvaluation(BaseModel):
    experience_years: float = Field(ge=0)
    meets_requirement: bool
    experience_score: int = Field(ge=0, le=100)


class SemanticEvaluation(BaseModel):
    semantic_match_score: int = Field(ge=0, le=100)
    rationale: str


class ATSEvaluation(BaseModel):
    ats_score: int = Field(ge=0, le=100)
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)


class FinalEvaluation(BaseModel):
    final_score: float = Field(ge=0, le=100)
    summary: str
    recommendation: str

    @field_validator("recommendation")
    @classmethod
    def normalize_recommendation(cls, value: str) -> str:
        allowed = {"Strong Match", "Good Match", "Moderate Match", "Weak Match"}
        label = value.strip()
        if label in allowed:
            return label
        lowered = label.lower()
        for candidate in allowed:
            if candidate.lower() in lowered:
                return candidate
        return "Moderate Match"


# Weighted scoring model (must total 100).
SCORE_WEIGHTS = {
    "skill": 0.40,
    "experience": 0.25,
    "semantic": 0.20,
    "ats": 0.15,
}
