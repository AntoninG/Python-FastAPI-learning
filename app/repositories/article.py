"""
Articles repository to manipulate Article models
"""

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..models.article import Article


def get_all(db: Session, params: dict) -> list[Article]:
    statement = db.query(Article)

    if 'query' in params and params['query'] is not None:
        query = params['query']
        statement = statement \
            .filter(Article.title.like(f'%{query}%'))

    if 'limit' in params and params['limit'] is not None:
        statement = statement.limit(params['limit'])

    if 'offset' in params and params['offset'] is not None:
        statement = statement.offset(params['offset'])

    return statement.all()


def get(db: Session, id_article: int) -> Article:
    article = db.query(Article).filter(Article.id == id_article).first()
    if not article:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    return article


def create(db: Session, request: dict) -> Article:
    article_dict = request.copy()
    if 'user_id' not in article_dict:
        article_dict.update({'user_id': 1})
    new_article = Article(**article_dict)

    try:
        db.add(new_article)
        db.commit()
        db.refresh(new_article)
    except IntegrityError as e:
        raise HTTPException(status.HTTP_409_CONFLICT) from e

    return new_article


def update(db: Session, id_article: int, request: dict) -> Article:
    article_query = db.query(Article).filter(Article.id == id_article)
    article = article_query.first()
    if not article:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    article_query.update(request)
    db.commit()
    db.refresh(article)

    return article


def delete(db: Session, id_article: int) -> bool:
    article = db.query(Article) \
        .filter(Article.id == id_article) \
        .delete(synchronize_session=False)

    if not article:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    db.commit()

    return True
