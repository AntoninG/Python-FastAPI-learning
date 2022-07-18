from pydantic import BaseModel


class CreateArticleRequest(BaseModel):
    title: str
    content: str
