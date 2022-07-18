from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    name: str
    email: str
    password: str


class PasswordVerifyRequest(BaseModel):
    password: str
