"""
Provides utilities functions for token handling
"""
from datetime import datetime, timedelta
from os import getenv

from jose import JWTError, jwt

from app.schemas.requests import TokenData


def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    expires = datetime.utcnow()
    expires += timedelta(minutes=float(getenv("ACCESS_TOKEN_EXPIRE_MIN")))

    to_encode.update({"exp": expires})
    return jwt.encode(
        to_encode,
        getenv("SECRET_KEY"),
        algorithm=getenv("JWT_ALGORITHM")
    )


def verify_token(token: str,
                 credentials_exception: Exception | None = None) -> TokenData:
    try:
        payload = jwt.decode(
            token,
            getenv("SECRET_KEY"),
            algorithms=[getenv("JWT_ALGORITHM")]
        )

        email: str = payload.get("username")
        if email is None:
            raise credentials_exception

        return TokenData(**payload)
    except JWTError as e:
        raise credentials_exception if credentials_exception is not None else e
