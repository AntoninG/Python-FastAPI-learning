from pydantic import BaseModel


class UserResource(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True


class ArticleResource(BaseModel):
    id: int
    title: str
    content: str

    class Config:
        orm_mode = True


class ReadArticleResource(ArticleResource):
    author: UserResource


class ReadUserResource(UserResource):
    articles: list[ArticleResource] = []


class PasswordVerifyResource(BaseModel):
    password: str
