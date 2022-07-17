from pydantic import BaseModel


class Article(BaseModel):
    title: str
    content: str


class ArticleResource(Article):
    id: int

    class Config:
        orm_mode = True


class User(BaseModel):
    name: str
    email: str
    password: str


class UserResource(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True


class PasswordVerify(BaseModel):
    password: str


class PasswordVerifyResource(BaseModel):
    password: str
