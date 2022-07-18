from fastapi import APIRouter, HTTPException, Path, Query, status

from app.utils.hashing import Hash

from app.repositories import user
from app.schemas.requests import CreateUserRequest, PasswordVerifyRequest
from app.schemas.resources import UserResource, ReadUserResource

router = APIRouter(prefix='/users', tags=['users'])


@router.post('/',
             summary='Create user',
             description='Register a user and returns its information',
             status_code=status.HTTP_201_CREATED,
             responses={
                 status.HTTP_201_CREATED: {'description': 'User created'},
                 status.HTTP_404_NOT_FOUND: {'description': 'User not found'}
             },
             response_model=UserResource)
def create(request: CreateUserRequest):
    return user.create(request.dict())


@router.get('/{id}',
            summary='Get user',
            description='Retrieve a user\'s information',
            status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_200_OK: {'description': 'User found'},
                status.HTTP_404_NOT_FOUND: {'description': 'User not found'}
            },
            response_model=ReadUserResource)
def read(id: int = Path(description="User ID")):
    return user.get(id)


@router.post('/verify-password',
             summary='Verify password',
             description='Verify the password provided',
             tags=['password'],
             status_code=status.HTTP_200_OK,
             responses={
                 status.HTTP_200_OK: {'description': 'Password verified'},
                 status.HTTP_404_NOT_FOUND: {'description': 'Email not found'},
                 status.HTTP_401_UNAUTHORIZED: {
                     'description': 'Wrong password'}
             })
def verify_password(request: PasswordVerifyRequest,
                    email: str = Query(description="Email to compare password with")):
    user_db = user.find({'email': email}, True)
    if not user_db:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    if not Hash.verify(request.password, user_db.password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    return True
