import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_company
from app.database.session import get_db
from app.models import Company
from app.schemas.main import ApplicationResponse, CandidateStatusUpdate
from app.services.candidate_service import CandidateService

router = APIRouter(prefix="/applications", tags=["applications"])


def get_candidate_service(company: Company = Depends(get_current_company), db: Session = Depends(get_db)) -> CandidateService:
    return CandidateService(db)


@router.get("", response_model=list[ApplicationResponse])
def list_applications(
    service: CandidateService = Depends(get_candidate_service),
    company: Company = Depends(get_current_company),
):
    return service.list_candidates_for_company(company.id)


@router.get("/{application_id}", response_model=ApplicationResponse)
def get_application(
    application_id: uuid.UUID,
    service: CandidateService = Depends(get_candidate_service),
    company: Company = Depends(get_current_company),
):
    return service.get_application_for_company(company.id, application_id)


@router.post("/{application_id}/status", response_model=ApplicationResponse)
def change_status(
    application_id: uuid.UUID,
    payload: CandidateStatusUpdate,
    service: CandidateService = Depends(get_candidate_service),
    company: Company = Depends(get_current_company),
):
    return service.change_candidate_status(company.id, application_id, payload.status)


@router.post("/{application_id}/retry")
def retry_processing(
    application_id: uuid.UUID,
    service: CandidateService = Depends(get_candidate_service),
    company: Company = Depends(get_current_company),
):
    """Re-queue AI processing for a failed application. Company-only, with ownership check."""
    from app.models import ProcessingStatus
    from app.tasks.resume_tasks import process_resume_task

    application = service.get_application_for_company(company.id, application_id)
    if application.processing_status == ProcessingStatus.PROCESSING:
        raise HTTPException(status.HTTP_409_CONFLICT, "Application is already being processed")

    service.applications.set_processing_status(application.id, ProcessingStatus.PROCESSING, None)
    process_resume_task.delay(str(application.id))
    return {"detail": "Processing re-queued", "application_id": str(application.id)}


@router.get("/{application_id}/resume")
def download_resume(
    application_id: uuid.UUID,
    service: CandidateService = Depends(get_candidate_service),
    company: Company = Depends(get_current_company),
):
    application = service.get_application_for_company(company.id, application_id)
    if application.resume is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Resume file not found")
    import os

    from app.core.config import settings

    absolute_path = os.path.join(str(settings.base_dir), application.resume.file_url.lstrip("/"))
    if not os.path.exists(absolute_path):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Resume file missing on server")
    return FileResponse(absolute_path, media_type="application/pdf", filename=application.resume.file_name)
