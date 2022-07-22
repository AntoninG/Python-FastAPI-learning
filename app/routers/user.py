"""
User routes
"""

from fastapi import (APIRouter, Depends, HTTPException, Path, Query, status)
from sqlalchemy.orm import Session

from app.main import get_db
from app.repositories import user
from app.schemas.requests import CreateUserRequest, PasswordVerifyRequest
from app.schemas.resources import ReadUserResource, UserResource
from app.utils.hashing import Hash

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/",
             summary="Create user",
             description="Register a user and returns its information",
             status_code=status.HTTP_201_CREATED,
             responses={
                 status.HTTP_201_CREATED: {"description": "User created"},
                 status.HTTP_404_NOT_FOUND: {"description": "User not found"}
             },
             response_model=UserResource)
def create(request: CreateUserRequest, db: Session = Depends(get_db)):
    return user.create(db, request.dict())


@router.get("/{id_user}",
            summary="Get user",
            description="Retrieve a user's information",
            status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_200_OK: {"description": "User found"},
                status.HTTP_404_NOT_FOUND: {"description": "User not found"}
            },
            response_model=ReadUserResource)
def read(
        id_user: int = Path(description="User ID"),
        db: Session = Depends(get_db)):
    return user.get(db, id_user)


@router.post("/verify-password",
             summary="Verify password",
             description="Verify the password provided",
             tags=["password"],
             status_code=status.HTTP_200_OK,
             responses={
                 status.HTTP_200_OK: {"description": "Password verified"},
                 status.HTTP_404_NOT_FOUND: {"description": "Email not found"},
                 status.HTTP_401_UNAUTHORIZED: {
                     "description": "Wrong password"}
             })
def verify_password(request: PasswordVerifyRequest,
                    email: str = Query(
                        description="Email to compare password with"
                    ),
                    db: Session = Depends(get_db)):
    """
    Verify the password provided compared with the password of the email
    provided.
    :param request: POST data with the plain password
    :param email: The user's login
    :param db: DB session
    :return: True if password is verified
    :raises: HTTPException with HTTP 401 if user not found or wrong password
    """
    user_db = user.find(db, {"email": email}, True)
    if not user_db:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    if not Hash.verify(request.password, user_db.password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    return True
