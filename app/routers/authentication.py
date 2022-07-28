"""
Authentication routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.main import get_db
from app.models.user import User
from app.repositories import user as user_repository
from app.schemas.resources import Token, UserPersonalInformationResource
from app.utils.hashing import Hash
from app.utils.oauth2 import current_user
from app.utils.token import create_access_token

router = APIRouter(tags=["Authentication"])


@router.post(
    "/login",
    summary="Login",
    description="Tries to authenticate",
    response_model=Token
)
def login(request: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)):
    """
    Login route to obtain JWT
    :param request: OAuth2 request
    :param db: DB connection
    :return: JWT
    """
    user = user_repository.find(db, {"email": request.username}, True)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if not Hash.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    access_token = create_access_token({
        "id": user.id,
        "username": user.email,
        "name": user.name,

    })
    return {"access_token": access_token, "token_type": "bearer"}


@router.get(
    "/me",
    summary="Me I and myself",
    description="Get connected user's personal information",
    response_model=UserPersonalInformationResource
)
def me_i_and_myself(user: User = Depends(current_user)):
    return user
