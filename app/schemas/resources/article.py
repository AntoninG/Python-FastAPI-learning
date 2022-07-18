from pydantic import BaseModel

from app.schemas.resources.user import UserResource


class ArticleResource(BaseModel):
    id: int
    title: str
    content: str

    class Config:
        orm_mode = True


class ReadArticleResource(ArticleResource):
    author: UserResource
