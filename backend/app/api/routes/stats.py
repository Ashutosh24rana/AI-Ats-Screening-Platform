from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_company
from app.database.session import get_db
from app.models import Company
from app.repositories.application_repository import ApplicationRepository

router = APIRouter(tags=["stats"])


@router.get("/jobs/{job_id}/applications")
def job_applications_ranked(
    job_id: str,
    company: Company = Depends(get_current_company),
    db: Session = Depends(get_db),
):
    from fastapi import HTTPException, status

    import uuid as _uuid

    try:
        parsed_job_id = _uuid.UUID(job_id)
    except ValueError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Job not found")

    from app.models import Job

    job = db.get(Job, parsed_job_id)
    if job is None or job.company_id != company.id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Job not found")

    repo = ApplicationRepository(db)
    applications = repo.list_for_job_sorted_by_score(parsed_job_id)
    counts = repo.counts_for_job(parsed_job_id)

    items = []
    for rank, application in enumerate(applications, start=1):
        score = application.score
        items.append(
            {
                "rank": rank,
                "application_id": str(application.id),
                "candidate_name": application.candidate.name,
                "candidate_email": application.candidate.email,
                "status": application.status,
                "processing_status": application.processing_status,
                "applied_at": application.applied_at,
                "final_score": score.final_score if score else None,
                "skill_score": score.skill_score if score else None,
                "experience_score": score.experience_score if score else None,
                "matched_skills": (score.matched_skills or [])[:6] if score else [],
            }
        )

    return {
        "job": {
            "id": str(job.id),
            "title": job.title,
            "description": job.description,
            "required_skills": job.required_skills or [],
            "preferred_skills": job.preferred_skills or [],
            "minimum_experience": job.minimum_experience,
            "location": job.location,
            "employment_type": job.employment_type,
            "application_slug": job.application_slug,
            "status": job.status,
        },
        "counts": counts,
        "candidates": items,
    }
