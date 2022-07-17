from fastapi import APIRouter, Path, Query, Depends, status, HTTPException
from sqlalchemy.orm import Session
from ..schemas import requests, resources
from .. import models, database

router = APIRouter(prefix='/articles', tags=['articles'])


@router.get('/',
            summary='Articles index',
            description='Retrieve all articles filled with their author',
            status_code=status.HTTP_200_OK,
            response_model=list[resources.ReadArticleResource])
def index(db: Session = Depends(database.get_db),
          limit: int | None = Query(1, description='Maximum size of results set'),
          offset: int = Query(0, description='Starting offset of results set'),
          query: str | None = Query(None, description='Title query')):
    statement = db.query(models.Article)

    if query is not None:
        statement = statement\
            .filter(models.Article.title.like('%{0}%'.format(query)))

    if limit is not None:
        statement = statement.limit(limit)

    if offset is not None:
        statement = statement.offset(offset)

    return statement.all()


@router.post('/',
             summary='Create article',
             description='Create article in DB',
             status_code=status.HTTP_201_CREATED,
             response_description='Article created',
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


@router.get('/{id}',
            summary='Get article',
            description='Retrieve a specific article filled with its author',
            status_code=status.HTTP_200_OK,
            responses={status.HTTP_404_NOT_FOUND: {'description': 'Article not found'}},
            response_model=resources.ReadArticleResource)
def read(id: int = Path(description='Article ID'),
         db: Session = Depends(database.get_db)):
    article = db.query(models.Article).filter(models.Article.id == id).first()

    if not article:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    return article


@router.put('/{id}',
            summary='Update article',
            description='Update an article by overriding all its data with request',
            status_code=status.HTTP_202_ACCEPTED,
            response_description='Article updated',
            responses={status.HTTP_404_NOT_FOUND: {'description': 'Article not found'}},
            response_model=resources.ArticleResource)
def update(request: requests.CreateArticleRequest,
           id: int = Path(description='Article ID'),
           db: Session = Depends(database.get_db)):
    article_query = db.query(models.Article).filter(models.Article.id == id)
    article = article_query.first()
    if not article:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    article_query.update(request.dict())
    db.commit()
    db.refresh(article)

    return article


@router.delete('/{id}',
               summary='Delete article',
               description='Delete an article by overriding all its data with request',
               status_code=status.HTTP_204_NO_CONTENT,
               response_description='Article deleted',
               responses={status.HTTP_404_NOT_FOUND: {'description': 'Article not found'}})
def delete(id: int = Path(description='Article ID'),
           db: Session = Depends(database.get_db)):
    article = db.query(models.Article) \
        .filter(models.Article.id == id) \
        .delete(synchronize_session=False)

    if not article:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    db.commit()
