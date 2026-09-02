import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import Job, JobStatus, Company
from app.repositories.job_repository import JobRepository
from app.schemas.main import JobCreate, JobUpdate


VALID_TRANSITIONS = {
    None: set(),
    "": set(),
}


class JobService:
    def __init__(self, db: Session, company: Company):
        self.db = db
        self.company = company
        self.jobs = JobRepository(db)

    def list_jobs(self) -> list[dict]:
        jobs = self.jobs.list_for_company(self.company.id)
        stats = self.jobs.stats_for_company(self.company.id)
        result = []
        for job in jobs:
            item = {
                "id": str(job.id),
                "title": job.title,
                "description": job.description,
                "required_skills": job.required_skills,
                "preferred_skills": job.preferred_skills,
                "minimum_experience": job.minimum_experience,
                "location": job.location,
                "employment_type": job.employment_type,
                "application_slug": job.application_slug,
                "status": job.status,
                "created_at": job.created_at,
            }
            item.update(stats.get(str(job.id), {}))
            result.append(item)
        return result

    def get_job(self, job_id: uuid.UUID) -> Job:
        job = self.jobs.get(job_id)
        if job is None or job.company_id != self.company.id:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Job not found")
        return job

    def create_job(self, payload: JobCreate) -> Job:
        job = self.jobs.create(company_id=self.company.id, status=JobStatus.DRAFT, **payload.model_dump())
        self.db.commit()
        return job

    def update_job(self, job_id: uuid.UUID, payload: JobUpdate) -> Job:
        job = self.get_job(job_id)
        data = payload.model_dump(exclude_unset=True)
        if "status" in data and data["status"] not in JobStatus.ALL:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, f"Status must be one of {JobStatus.ALL}")
        updated = self.jobs.update(job, **data)
        self.db.commit()
        return updated

    def change_status(self, job_id: uuid.UUID, new_status: str) -> Job:
        job = self.get_job(job_id)
        if new_status not in JobStatus.ALL:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, f"Status must be one of {JobStatus.ALL}")
        updated = self.jobs.update(job, status=new_status)
        self.db.commit()
        return updated

    def delete_job(self, job_id: uuid.UUID) -> None:
        job = self.get_job(job_id)
        self.db.delete(job)
        self.db.commit()
