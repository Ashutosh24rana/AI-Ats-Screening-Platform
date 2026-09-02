import uuid

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.database.session import get_db
from app.models import Company, User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"/api/v1/auth/login")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid authentication credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    user_id = decode_access_token(token)
    if user_id is None:
        raise credentials_exception
    try:
        parsed_id = uuid.UUID(user_id)
    except ValueError:
        raise credentials_exception
    user = db.get(User, parsed_id)
    if user is None:
        raise credentials_exception
    return user


def get_current_company(user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> Company:
    company = db.query(Company).filter(Company.user_id == user.id).first()
    if company is None:
        raise HTTPException(status_code=404, detail="Company profile not found for this account")
    return company
