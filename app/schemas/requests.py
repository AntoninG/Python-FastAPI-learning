from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    name: str
    email: str
    password: str


class CreateArticleRequest(BaseModel):
    title: str
    content: str


class PasswordVerifyRequest(BaseModel):
    password: str
