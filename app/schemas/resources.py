"""
Resources schemas answered by the app
"""

from pydantic import BaseModel, SecretStr


# pylint: disable=too-few-public-methods
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


class Token(BaseModel):
    access_token: str
    token_type: str


class UserPersonalInformationResource(ReadUserResource):
    password: SecretStr
