import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_company
from app.database.session import get_db
from app.models import Company
from app.repositories.application_repository import ApplicationRepository
from app.schemas.main import ApplicationResponse
from app.services.candidate_service import CandidateService

router = APIRouter(prefix="/candidates", tags=["candidates"])


@router.get("/applications", response_model=list[ApplicationResponse])
def list_candidates(
    company: Company = Depends(get_current_company),
    db: Session = Depends(get_db),
):
    """All candidates who applied to this company's jobs, newest first."""
    applications = ApplicationRepository(db).list_for_company(company.id)
    return applications


@router.get("/dashboard-stats")
def dashboard_stats(
    company: Company = Depends(get_current_company),
    db: Session = Depends(get_db),
):
    from app.models import Application, ApplicationStatus, Job
    from sqlalchemy import func, case

    total_jobs = db.query(func.count(Job.id)).filter(Job.company_id == company.id).scalar() or 0
    active_jobs = (
        db.query(func.count(Job.id)).filter(Job.company_id == company.id, Job.status == "PUBLISHED").scalar() or 0
    )
    shortlisted_expr = func.sum(case((Application.status == ApplicationStatus.SHORTLISTED, 1), else_=0))
    rows = (
        db.query(func.count(Application.id), shortlisted_expr)
        .join(Job, Job.id == Application.job_id)
        .filter(Job.company_id == company.id)
        .first()
    )
    return {
        "total_jobs": int(total_jobs),
        "active_jobs": int(active_jobs),
        "total_applications": int(rows[0] or 0),
        "shortlisted": int(rows[1] or 0),
    }
