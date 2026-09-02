from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_company
from app.database.session import get_db
from app.models import Company
from app.schemas.main import CompanyResponse, CompanyUpdate
from app.services.company_service import CompanyService

router = APIRouter(prefix="/companies", tags=["companies"])


@router.get("/me", response_model=CompanyResponse)
def get_my_company(company: Company = Depends(get_current_company)):
    return company


@router.patch("/me", response_model=CompanyResponse)
def update_my_company(
    payload: CompanyUpdate,
    company: Company = Depends(get_current_company),
    db: Session = Depends(get_db),
):
    return CompanyService(db, company).update_profile(payload)
