from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .. import database
from ..models.article import Article

db: Session = database.SessionLocal()


def get_all(params: dict) -> list[Article]:
    statement = db.query(Article)

    if 'query' in params and params['query'] is not None:
        statement = statement \
            .filter(Article.title.like('%{0}%'.format(params['query'])))

    if 'limit' in params and params['limit'] is not None:
        statement = statement.limit(params['limit'])

    if 'offset' in params and params['offset'] is not None:
        statement = statement.offset(params['offset'])

    return statement.all()


def get(id: int) -> Article:
    article = db.query(Article).filter(Article.id == id).first()
    if not article:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    return article


def create(request: dict) -> Article:
    article_dict = request.copy()
    article_dict.update({'user_id': 1})
    new_article = Article(**article_dict)

    db.add(new_article)
    db.commit()
    db.refresh(new_article)

    return new_article


def update(id: int, request: dict) -> Article:
    article_query = db.query(Article).filter(Article.id == id)
    article = article_query.first()
    if not article:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    article_query.update(request)
    db.commit()
    db.refresh(article)

    return article


def delete(id: int) -> bool:
    article = db.query(Article) \
        .filter(Article.id == id) \
        .delete(synchronize_session=False)

    if not article:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    db.commit()

    return True
