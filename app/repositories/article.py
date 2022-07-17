from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from .. import models, database

db: Session = database.SessionLocal()


def get_all(params: dict) -> list[models.Article]:
    statement = db.query(models.Article)

    if 'query' in params and params['query'] is not None:
        statement = statement \
            .filter(models.Article.title.like('%{0}%'.format(params['query'])))

    if 'limit' in params and params['limit'] is not None:
        statement = statement.limit(params['limit'])

    if 'offset' in params and params['offset'] is not None:
        statement = statement.offset(params['offset'])

    return statement.all()


def get(id: int) -> models.Article:
    article = db.query(models.Article).filter(models.Article.id == id).first()
    if not article:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    return article


def create(request: dict) -> models.Article:
    article_dict = request.copy()
    article_dict.update({'user_id': 1})
    new_article = models.Article(**article_dict)

    db.add(new_article)
    db.commit()
    db.refresh(new_article)

    return new_article


def update(id: int, request: dict) -> models.Article:
    article_query = db.query(models.Article).filter(models.Article.id == id)
    article = article_query.first()
    if not article:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    article_query.update(request)
    db.commit()
    db.refresh(article)

    return article


def delete(id: int) -> bool:
    article = db.query(models.Article) \
        .filter(models.Article.id == id) \
        .delete(synchronize_session=False)

    if not article:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    db.commit()

    return True
