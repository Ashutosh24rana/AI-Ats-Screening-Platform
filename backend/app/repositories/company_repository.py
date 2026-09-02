import uuid

from sqlalchemy.orm import Session

from app.models import Company


class CompanyRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_user_id(self, user_id: uuid.UUID) -> Company | None:
        return self.db.query(Company).filter(Company.user_id == user_id).first()

    def create(
        self,
        user_id: uuid.UUID,
        company_name: str,
        description: str | None = None,
        website: str | None = None,
        logo_url: str | None = None,
    ) -> Company:
        company = Company(
            user_id=user_id,
            company_name=company_name,
            description=description,
            website=website,
            logo_url=logo_url,
        )
        self.db.add(company)
        self.db.flush()
        return company
