from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from ..schemas import requests, resources
from .. import models, database

router = APIRouter(prefix='/articles', tags=['articles', 'core'])


@router.get('/', status_code=status.HTTP_200_OK,
            response_model=list[resources.ReadArticleResource])
def index(db: Session = Depends(database.get_db)):
    return db.query(models.Article).all()


@router.post('/', status_code=status.HTTP_201_CREATED,
             response_model=resources.ArticleResource)
def create(request: requests.CreateArticleRequest,
           db: Session = Depends(database.get_db)):
    article_dict = request.dict()
    article_dict.update({'user_id': 1})
    new_article = models.Article(**article_dict)

    db.add(new_article)
    db.commit()
    db.refresh(new_article)

    return new_article


@router.get('/{id}', status_code=status.HTTP_200_OK,
            response_model=resources.ReadArticleResource)
def read(id: int, db: Session = Depends(database.get_db)):
    article = db.query(models.Article).filter(models.Article.id == id).first()

    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return article


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED,
            response_model=resources.ArticleResource)
def update(id: int, request: requests.CreateArticleRequest,
           db: Session = Depends(database.get_db)):
    article_query = db.query(models.Article).filter(models.Article.id == id)
    article = article_query.first()
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    article_query.update(request.dict())
    db.commit()
    db.refresh(article)

    return article


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(database.get_db)):
    article = db.query(models.Article) \
        .filter(models.Article.id == id) \
        .delete(synchronize_session=False)

    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    db.commit()
