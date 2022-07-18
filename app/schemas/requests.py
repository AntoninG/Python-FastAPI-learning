from pydantic import BaseModel, EmailStr, SecretStr


class CreateArticleRequest(BaseModel):
    title: str
    content: str


class CreateUserRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class PasswordVerifyRequest(BaseModel):
    password: str
