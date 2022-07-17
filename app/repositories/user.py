from typing import Union
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from .. import models, database
from ..hashing import Hash

db: Session = database.SessionLocal()


def get(id: int) -> models.User:
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    return user


def create(request: dict) -> models.User:
    request_dict = request
    request_dict['password'] = Hash.bcrypt(request['password'])

    user = models.User(**request_dict)
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def find(params: dict, single: bool = False) -> models.User | list[models.User] | None:
    statement = db.query(models.User)

    if 'email' in params:
        statement = statement.filter(models.User.email == params['email'])

    return statement.all() if not single else statement.first()
