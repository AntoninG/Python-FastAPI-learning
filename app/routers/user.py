from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from ..schemas import requests, resources
from ..hashing import Hash
from .. import models, database

router = APIRouter(prefix='/users', tags=['users'])


@router.post('/', status_code=status.HTTP_201_CREATED,
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


@router.get('/{id}', status_code=status.HTTP_200_OK,
            response_model=resources.ReadUserResource)
def read_user(id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return user


@router.post('/{id}/verify-password', tags=['password'],
             status_code=status.HTTP_200_OK,
             response_model=resources.PasswordVerifyResource)
def verify_password(id: int, request: requests.PasswordVerifyRequest,
                    db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return {'password': Hash.verify(request.password, user.password)}
