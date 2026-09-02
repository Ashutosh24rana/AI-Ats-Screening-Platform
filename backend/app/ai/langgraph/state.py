from typing import Annotated, TypedDict

from app.ai.evaluation.evaluation_schemas import (
    ATSEvaluation,
    ExperienceEvaluation,
    FinalEvaluation,
    SemanticEvaluation,
    SkillEvaluation,
)


class EvaluationState(TypedDict, total=False):
    # Inputs
    application_id: str
    job_id: str
    candidate_id: str
    resume_id: str
    resume_file_path: str
    job_title: str
    job_description: str
    required_skills: list[str]
    preferred_skills: list[str]
    minimum_experience: int

    # Intermediate
    resume_text: str
    resume_context: str
    skill_result: SkillEvaluation
    experience_result: ExperienceEvaluation
    semantic_result: SemanticEvaluation
    ats_result: ATSEvaluation

    # Outputs
    result: FinalEvaluation | None
    error: str | None
