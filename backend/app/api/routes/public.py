from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models import Company, Job, JobStatus
from app.schemas.main import ApplicationResponse, PublicJobResponse
from app.services.application_service import ApplicationService

router = APIRouter(prefix="/public", tags=["public"])


def _get_published_job(db: Session, slug: str) -> tuple[Job, Company]:
    row = (
        db.query(Job, Company)
        .join(Company, Company.id == Job.company_id)
        .filter(Job.application_slug == slug)
        .first()
    )
    if row is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Application link not found")
    job, company = row
    if job.status != JobStatus.PUBLISHED:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "This job is no longer accepting applications")
    return job, company


@router.get("/jobs/{slug}", response_model=PublicJobResponse)
def get_public_job(slug: str, db: Session = Depends(get_db)):
    """Public job details. No authentication required."""
    job, company = _get_published_job(db, slug)
    return PublicJobResponse(
        title=job.title,
        description=job.description,
        required_skills=job.required_skills or [],
        preferred_skills=job.preferred_skills or [],
        minimum_experience=job.minimum_experience,
        location=job.location,
        employment_type=job.employment_type,
        company_name=company.company_name,
    )


@router.post("/jobs/{slug}/apply", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
def apply_to_job(
    slug: str,
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(None),
    resume: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """Public application submission (multipart/form-data). No authentication."""
    # Validate job exists and is published before doing any work.
    _get_published_job(db, slug)
    service = ApplicationService(db)
    application = service.submit_public_application(slug=slug, name=name, email=email, phone=phone, resume=resume)
    return application
