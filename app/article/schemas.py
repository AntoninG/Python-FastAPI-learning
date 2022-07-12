from pydantic import BaseModel


class Article(BaseModel):
    title: str
    content: str


class ArticleResource(Article):
    id: int

    class Config:
        orm_mode = True
