import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_company
from app.database.session import get_db
from app.models import Company
from app.schemas.main import JobCreate, JobResponse, JobStatusUpdate, JobUpdate, JobWithStats
from app.services.job_service import JobService

router = APIRouter(prefix="/jobs", tags=["jobs"])


def get_job_service(company: Company = Depends(get_current_company), db: Session = Depends(get_db)) -> JobService:
    return JobService(db, company)


@router.get("", response_model=list[JobWithStats])
def list_jobs(service: JobService = Depends(get_job_service)):
    return service.list_jobs()


@router.post("", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
def create_job(payload: JobCreate, service: JobService = Depends(get_job_service)):
    return service.create_job(payload)


@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: uuid.UUID, service: JobService = Depends(get_job_service)):
    return service.get_job(job_id)


@router.patch("/{job_id}", response_model=JobResponse)
def update_job(job_id: uuid.UUID, payload: JobUpdate, service: JobService = Depends(get_job_service)):
    return service.update_job(job_id, payload)


@router.post("/{job_id}/status", response_model=JobResponse)
def change_status(job_id: uuid.UUID, payload: JobStatusUpdate, service: JobService = Depends(get_job_service)):
    return service.change_status(job_id, payload.status)


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(job_id: uuid.UUID, service: JobService = Depends(get_job_service)):
    service.delete_job(job_id)
