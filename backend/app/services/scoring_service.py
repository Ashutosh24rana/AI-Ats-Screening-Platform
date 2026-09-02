from sqlalchemy.orm import Session, joinedload

from app.ai.langgraph.workflow import build_evaluation_workflow
from app.models import Application, CandidateScore, Job
from app.repositories.application_repository import ApplicationRepository


class ScoringService:
    """Runs the LangGraph evaluation workflow and persists structured results."""

    def __init__(self, db: Session):
        self.db = db
        self.applications = ApplicationRepository(db)

    def evaluate_application(self, application_id) -> CandidateScore | None:
        application = (
            self.db.query(Application)
            .options(
                joinedload(Application.job),
                joinedload(Application.candidate),
                joinedload(Application.resume),
            )
            .filter(Application.id == application_id)
            .first()
        )
        if application is None or application.resume is None:
            return None

        from pathlib import Path

        from app.core.config import settings

        resume_path = Path(application.resume.file_url.lstrip("/"))
        if not resume_path.is_absolute():
            resume_path = Path(settings.base_dir) / resume_path

        job: Job = application.job
        workflow = build_evaluation_workflow()
        final_state = workflow.invoke(
            {
                "application_id": str(application.id),
                "job_id": str(job.id),
                "candidate_id": str(application.candidate_id),
                "resume_id": str(application.resume_id),
                "resume_file_path": str(resume_path),
                "job_title": job.title,
                "job_description": job.description,
                "required_skills": list(job.required_skills or []),
                "preferred_skills": list(job.preferred_skills or []),
                "minimum_experience": job.minimum_experience,
            }
        )

        # A graph-level error (e.g. unreadable file) should fail fast, not retry-loop.
        error_message = final_state.get("error")
        result = final_state.get("result")
        if result is None:
            raise RuntimeError(error_message or "Evaluation produced no result")

        skill = final_state["skill_result"]
        experience = final_state["experience_result"]
        semantic = final_state["semantic_result"]
        ats = final_state["ats_result"]

        score = self.applications.db.query(CandidateScore).filter(
            CandidateScore.application_id == application.id
        ).first()
        if score is None:
            score = CandidateScore(application_id=application.id)
            self.db.add(score)

        score.skill_score = skill.skill_score
        score.experience_score = experience.experience_score
        score.ats_score = ats.ats_score
        score.semantic_match_score = semantic.semantic_match_score
        score.final_score = result.final_score
        score.matched_skills = skill.matched_skills
        score.missing_skills = skill.missing_skills
        score.strengths = final_state.get("strengths", [])
        score.weaknesses = final_state.get("weaknesses", [])
        score.ai_summary = result.summary
        score.recommendation = result.recommendation

        # Shortlisting decision based on configured thresholds.
        from app.core.config import settings

        if result.final_score >= settings.shortlist_threshold:
            application.status = "SHORTLISTED"
        elif result.final_score >= settings.review_threshold:
            application.status = "REVIEW"
        else:
            application.status = "REJECTED"
        application.processing_status = "COMPLETED"
        application.processing_error = None

        self.db.commit()
        return score
