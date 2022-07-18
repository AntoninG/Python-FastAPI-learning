from pydantic import BaseModel

from .article import ArticleResource


class UserResource(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True


class ReadUserResource(UserResource):
    articles: list[ArticleResource] = []
