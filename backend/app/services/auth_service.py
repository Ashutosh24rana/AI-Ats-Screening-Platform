from fastapi import HTTPException, status

from app.core.security import create_access_token, hash_password, verify_password
from app.repositories.company_repository import CompanyRepository
from app.repositories.user_repository import UserRepository
from app.schemas.main import LoginRequest, RegisterRequest


class AuthService:
    def __init__(self, db):
        self.users = UserRepository(db)
        self.companies = CompanyRepository(db)

    def register(self, payload: RegisterRequest) -> str:
        if len(payload.password) < 8:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "Password must be at least 8 characters")
        if self.users.get_by_email(payload.email) is not None:
            raise HTTPException(status.HTTP_409_CONFLICT, "An account with this email already exists")

        user = self.users.create(email=payload.email, password_hash=hash_password(payload.password))
        self.companies.create(
            user_id=user.id,
            company_name=payload.company_name.strip(),
            description=payload.description,
            website=payload.website,
        )
        self.users.db.commit()
        return create_access_token(str(user.id))

    def login(self, payload: LoginRequest) -> str:
        user = self.users.get_by_email(payload.email)
        if user is None or not verify_password(payload.password, user.password_hash):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid email or password")
        return create_access_token(str(user.id))
