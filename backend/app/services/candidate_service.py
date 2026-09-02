from sqlalchemy.orm import Session, joinedload

from app.models import Application, ApplicationStatus, CandidateScore
from app.repositories.application_repository import ApplicationRepository


class CandidateService:
    """Company-facing views of candidates (public applicants) and their scores."""

    def __init__(self, db: Session):
        self.db = db
        self.applications = ApplicationRepository(db)

    def list_candidates_for_company(self, company_id):
        return self.applications.list_for_company(company_id)

    def get_application_for_company(self, company_id, application_id) -> Application:
        application = (
            self.db.query(Application)
            .options(joinedload(Application.candidate), joinedload(Application.job), joinedload(Application.score))
            .join(Application.job)
            .filter(Application.id == application_id)
            .first()
        )
        # ownership check via job.company_id resolved lazily to avoid circular import
        if application is None or application.job.company_id != company_id:
            from fastapi import HTTPException, status

            raise HTTPException(status.HTTP_404_NOT_FOUND, "Application not found")
        return application

    def change_candidate_status(self, company_id, application_id, new_status: str) -> Application:
        if new_status not in ApplicationStatus.ALL:
            from fastapi import HTTPException, status

            raise HTTPException(
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                f"Status must be one of {ApplicationStatus.ALL}",
            )
        application = self.get_application_for_company(company_id, application_id)
        return self.applications.set_status(application.id, new_status)

    def dashboard_stats(self, company_id) -> dict:
        jobs = self.applications.list_for_company(company_id)
        applications = jobs
        return {
            "total_jobs": len({str(a.job_id) for a in applications}),
            "total_applications": len(applications),
            "shortlisted": sum(1 for a in applications if a.status == ApplicationStatus.SHORTLISTED),
        }
