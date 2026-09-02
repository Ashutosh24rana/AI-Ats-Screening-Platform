import uuid

from sqlalchemy import case
from sqlalchemy.orm import Session, joinedload

from app.models import Application, ApplicationStatus, Candidate, CandidateScore, Job, ProcessingStatus


class ApplicationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, application_id: uuid.UUID) -> Application | None:
        return self.db.get(Application, application_id)

    def get_with_relations(self, application_id: uuid.UUID) -> Application | None:
        return (
            self.db.query(Application)
            .options(joinedload(Application.candidate), joinedload(Application.job), joinedload(Application.score))
            .filter(Application.id == application_id)
            .first()
        )

    def exists_for_job_and_candidate(self, job_id: uuid.UUID, candidate_id: uuid.UUID) -> bool:
        return (
            self.db.query(Application.id)
            .filter(Application.job_id == job_id, Application.candidate_id == candidate_id)
            .first()
            is not None
        )

    def create(self, job: Job, candidate: Candidate, resume_id: uuid.UUID | None) -> Application:
        application = Application(job=job, candidate=candidate, resume_id=resume_id)
        self.db.add(application)
        self.db.flush()
        return application

    def list_for_job_sorted_by_score(self, job_id: uuid.UUID) -> list[Application]:
        status_order = case(
            (Application.status == ApplicationStatus.SHORTLISTED, 1),
            (Application.status == ApplicationStatus.REVIEW, 2),
            (Application.status == ApplicationStatus.SCREENING, 3),
            (Application.status == ApplicationStatus.PENDING, 4),
            else_=5,
        )
        return (
            self.db.query(Application)
            .options(joinedload(Application.candidate), joinedload(Application.score))
            .outerjoin(CandidateScore, CandidateScore.application_id == Application.id)
            .filter(Application.job_id == job_id)
            .order_by(status_order, CandidateScore.final_score.desc().nullslast(), Application.applied_at.desc())
            .all()
        )

    def list_for_company(self, company_id: uuid.UUID) -> list[Application]:
        return (
            self.db.query(Application)
            .join(Job, Job.id == Application.job_id)
            .options(joinedload(Application.candidate), joinedload(Application.job), joinedload(Application.score))
            .filter(Job.company_id == company_id)
            .order_by(Application.applied_at.desc())
            .all()
        )

    def set_processing_status(
        self, application_id: uuid.UUID, status_value: str, error: str | None = None
    ) -> None:
        application = self.db.get(Application, application_id)
        if application is None:
            return
        application.processing_status = status_value
        application.processing_error = error
        if status_value == ProcessingStatus.PROCESSING and application.status in (
            ApplicationStatus.PENDING,
        ):
            application.status = ApplicationStatus.SCREENING
        self.db.commit()

    def set_status(self, application_id: uuid.UUID, status_value: str) -> Application | None:
        if status_value not in ApplicationStatus.ALL:
            return None
        application = self.db.get(Application, application_id)
        if application is None:
            return None
        application.status = status_value
        self.db.commit()
        self.db.refresh(application)
        return application

    def counts_for_job(self, job_id: uuid.UUID) -> dict[str, int]:
        applications = self.db.query(Application).filter(Application.job_id == job_id).all()
        return {
            "total": len(applications),
            "shortlisted": sum(1 for a in applications if a.status == ApplicationStatus.SHORTLISTED),
            "review": sum(1 for a in applications if a.status == ApplicationStatus.REVIEW),
            "rejected": sum(1 for a in applications if a.status == ApplicationStatus.REJECTED),
        }
