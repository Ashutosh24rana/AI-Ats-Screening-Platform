import os
import uuid

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models import Application, Candidate, Company, Job, JobStatus, ProcessingStatus
from app.repositories.application_repository import ApplicationRepository
from app.repositories.candidate_repository import CandidateRepository
from app.utils.file_utils import build_upload_path, safe_filename, validate_pdf_upload


class DuplicateApplicationError(Exception):
    pass


class ApplicationService:
    def __init__(self, db: Session):
        self.db = db
        self.applications = ApplicationRepository(db)
        self.candidates = CandidateRepository(db)

    def submit_public_application(
        self,
        slug: str,
        name: str,
        email: str,
        phone: str | None,
        resume: UploadFile,
    ) -> Application:
        job = self.db.query(Job).filter(Job.application_slug == slug).first()
        if job is None or job.status != JobStatus.PUBLISHED:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Application link is invalid or this job is not accepting applications")

        validate_pdf_upload(resume, max_size_mb=settings.max_upload_size_mb)

        candidate: Candidate = self.candidates.get_or_create(name=name, email=email, phone=phone)

        if self.applications.exists_for_job_and_candidate(job.id, candidate.id):
            raise HTTPException(status.HTTP_409_CONFLICT, "You have already applied for this position.")

        resume_record = self._save_resume(candidate.id, resume)
        application = self.applications.create(job=job, candidate=candidate, resume_id=resume_record.id)
        application.status = "SCREENING"
        application.processing_status = ProcessingStatus.PROCESSING
        self.db.commit()

        # Queue asynchronous AI processing through Celery (Redis broker).
        from app.tasks.resume_tasks import process_resume_task

        process_resume_task.delay(str(application.id))

        return application

    def _save_resume(self, candidate_id: uuid.UUID, upload: UploadFile):
        from app.models import Resume

        stored_name = safe_filename(upload.filename or "resume.pdf")
        relative_path = build_upload_path(settings.upload_dir, str(candidate_id), stored_name)
        os.makedirs(os.path.dirname(relative_path.absolute_path), exist_ok=True)

        file_size = 0
        with open(relative_path.absolute_path, "wb") as buffer:
            while chunk := upload.file.read(1024 * 1024):
                file_size += len(chunk)
                if file_size > settings.max_upload_size_mb * 1024 * 1024:
                    buffer.close()
                    os.remove(relative_path.absolute_path)
                    raise HTTPException(
                        status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        f"Resume must be smaller than {settings.max_upload_size_mb}MB",
                    )
                buffer.write(chunk)

        record = Resume(
            candidate_id=candidate_id,
            file_name=stored_name,
            file_url=relative_path.url_path,
        )
        self.db.add(record)
        self.db.flush()
        return record


def get_company_applications(db: Session, company: Company) -> list[Application]:
    return ApplicationRepository(db).list_for_company(company.id)


def get_company_application(db: Session, company: Company, application_id: uuid.UUID) -> Application:
    application = (
        db.query(Application).join(Job).filter(Application.id == application_id, Job.company_id == company.id).first()
    )
    if application is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Application not found")
    return application
