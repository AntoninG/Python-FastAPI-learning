"""
Users repository to manipulate User models
"""

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.utils.hashing import Hash

from ..models.user import User


def get(db: Session, id_user: int) -> User:
    user = db.query(User).filter(User.id == id_user).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    return user


def create(db: Session, request: dict) -> User:
    request_dict = request
    request_dict['password'] = Hash.bcrypt(request['password'])

    user = User(**request_dict)

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except IntegrityError as e:
        raise HTTPException(status.HTTP_304_NOT_MODIFIED) from e

    return user


def find(db: Session, params: dict, single: bool = False) -> User | list[User]\
                                                             | None:
    statement = db.query(User)

    if 'email' in params:
        statement = statement.filter(User.email == params['email'])

    return statement.all() if not single else statement.first()
