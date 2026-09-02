from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_company
from app.database.session import get_db
from app.models import Company
from app.schemas.main import CompanyUpdate


class CompanyService:
    def __init__(self, db: Session, company: Company):
        self.db = db
        self.company = company

    def get_profile(self) -> Company:
        return self.company

    def update_profile(self, payload: CompanyUpdate) -> Company:
        data = payload.model_dump(exclude_unset=True)
        for field, value in data.items():
            setattr(self.company, field, value)
        self.db.commit()
        self.db.refresh(self.company)
        return self.company


def get_company_service(
    company: Company = Depends(get_current_company), db: Session = Depends(get_db)
) -> CompanyService:
    return CompanyService(db, company)
