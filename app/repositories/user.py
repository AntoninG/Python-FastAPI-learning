from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.utils.hashing import Hash

from .. import database
from ..models.user import User

db: Session = database.SessionLocal()


def get(id: int) -> User:
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    return user


def create(request: dict) -> User:
    request_dict = request
    request_dict['password'] = Hash.bcrypt(request['password'])

    user = User(**request_dict)
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def find(params: dict, single: bool = False) -> User | list[
    User] | None:
    statement = db.query(User)

    if 'email' in params:
        statement = statement.filter(User.email == params['email'])

    return statement.all() if not single else statement.first()
