from pydantic import BaseModel


class ArticleResource(BaseModel):
    id: int
    title: str
    content: str

    class Config:
        orm_mode = True


class UserResource(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True


class ReadUserResource(UserResource):
    articles: list[ArticleResource] = []


class ReadArticleResource(ArticleResource):
    author: UserResource
