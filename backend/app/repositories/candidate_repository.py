from sqlalchemy import asc
from sqlalchemy.orm import Session, joinedload

from app.models import Candidate


class CandidateRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, candidate_id) -> Candidate | None:
        return self.db.get(Candidate, candidate_id)

    def get_by_email(self, email: str) -> Candidate | None:
        return self.db.query(Candidate).filter(asc(Candidate.email) == email.strip().lower()).first()

    def get_or_create(self, name: str, email: str, phone: str | None = None) -> Candidate:
        normalized_email = email.strip().lower()
        candidate = (
            self.db.query(Candidate).filter(Candidate.email == normalized_email).first()
        )
        if candidate is None:
            candidate = Candidate(name=name.strip(), email=normalized_email, phone=phone)
            self.db.add(candidate)
            self.db.flush()
        elif phone and not candidate.phone:
            candidate.phone = phone
            self.db.flush()
        return candidate
