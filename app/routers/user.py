from fastapi import APIRouter, Path, Query, Depends, status, HTTPException
from sqlalchemy.orm import Session
from ..schemas import requests, resources
from ..hashing import Hash
from .. import models, database

router = APIRouter(prefix='/users', tags=['users'])


@router.post('/',
             summary='Create user',
             description='Register a user and returns its information',
             status_code=status.HTTP_201_CREATED,
             responses={
                 status.HTTP_201_CREATED: {'description': 'User created'},
                 status.HTTP_404_NOT_FOUND: {'description': 'User not found'}
             },
             response_model=resources.UserResource)
def create_user(request: requests.CreateUserRequest,
                db: Session = Depends(database.get_db)):
    request_dict = request.dict()
    request_dict['password'] = Hash.bcrypt(request.password)

    user = models.User(**request_dict)
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.get('/{id}',
            summary='Get user',
            description='Retrieve a user\'s information',
            status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_200_OK: {'description': 'User found'},
                status.HTTP_404_NOT_FOUND: {'description': 'User not found'}
            },
            response_model=resources.ReadUserResource)
def read_user(
        id: int = Path(description="User ID"),
        db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    return user


@router.post('/verify-password',
             summary='Verify password',
             description='Verify the password provided',
             tags=['password'],
             status_code=status.HTTP_200_OK,
             responses={
                 status.HTTP_200_OK: {'description': 'Password verified'},
                 status.HTTP_404_NOT_FOUND: {'description': 'Email not found'},
                 status.HTTP_401_UNAUTHORIZED: {'description': 'Wrong password'}
             })
def verify_password(request: requests.PasswordVerifyRequest,
                    email: str = Query(description="Email to compare password with"),
                    db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    if not Hash.verify(request.password, user.password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    return True
