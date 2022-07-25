"""
Provides utilities for OAuth 2
"""
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.exceptions.http_exceptions import CredentialsException
from app.utils import token as token_util

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def current_user(token: str = Depends(oauth2_scheme)):
    return token_util.verify_token(token, CredentialsException())
