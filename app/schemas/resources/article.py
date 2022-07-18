from pydantic import BaseModel

from .user import UserResource


class ArticleResource(BaseModel):
    id: int
    title: str
    content: str

    class Config:
        orm_mode = True


class ReadArticleResource(ArticleResource):
    author: UserResource
