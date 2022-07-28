"""
Provides utilities for OAuth 2
"""
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.exceptions.http_exceptions import CredentialsException
from app.main import get_db
from app.models.user import User
from app.repositories import user as user_repository
from app.utils import token as token_util

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def current_user(token: str = Depends(oauth2_scheme),
                 db: Session = Depends(get_db)) -> User:
    token_data = token_util.verify_token(token, CredentialsException())
    return user_repository.get(db, token_data.id)
