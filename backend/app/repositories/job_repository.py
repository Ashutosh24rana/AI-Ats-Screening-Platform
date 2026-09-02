import uuid

from sqlalchemy import Integer, cast, func
from sqlalchemy.orm import Session

from app.models import Application, ApplicationStatus, CandidateScore, Job
from app.utils.id_generator import short_slug


class JobRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, job_id: uuid.UUID) -> Job | None:
        return self.db.get(Job, job_id)

    def get_by_slug(self, slug: str) -> Job | None:
        return self.db.query(Job).filter(Job.application_slug == slug).first()

    def list_for_company(self, company_id: uuid.UUID) -> list[Job]:
        return (
            self.db.query(Job)
            .filter(Job.company_id == company_id)
            .order_by(Job.created_at.desc())
            .all()
        )

    def create(self, company_id: uuid.UUID, **kwargs) -> Job:
        kwargs.pop("application_slug", None)
        job = Job(company_id=company_id, application_slug=short_slug(8), **kwargs)
        self.db.add(job)
        self.db.flush()
        return job

    def update(self, job: Job, **kwargs) -> Job:
        for field, value in kwargs.items():
            if value is not None and hasattr(job, field):
                setattr(job, field, value)
        self.db.flush()
        return job

    def stats_for_company(self, company_id: uuid.UUID) -> dict[str, dict]:
        """Per-job stats: applications count, shortlisted count, average score."""
        rows = (
            self.db.query(
                Application.job_id,
                func.count(Application.id).label("applications_count"),
                func.sum(cast(Application.status == ApplicationStatus.SHORTLISTED, Integer)).label("shortlisted_count"),
                func.avg(CandidateScore.final_score).label("average_score"),
            )
            .join(Job, Job.id == Application.job_id)
            .outerjoin(CandidateScore, CandidateScore.application_id == Application.id)
            .filter(Job.company_id == company_id)
            .group_by(Application.job_id)
            .all()
        )
        return {
            str(row.job_id): {
                "applications_count": int(row.applications_count or 0),
                "shortlisted_count": int(row.shortlisted_count or 0),
                "average_score": round(float(row.average_score), 1) if row.average_score is not None else None,
            }
            for row in rows
        }
