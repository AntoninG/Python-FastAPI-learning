from fastapi import APIRouter, Depends, Path, Query, status
from sqlalchemy.orm import Session

from app.main import get_db
from app.repositories import article as article_repository
from app.schemas.requests import CreateArticleRequest
from app.schemas.resources import ArticleResource, ReadArticleResource

router = APIRouter(prefix='/articles', tags=['articles'])


@router.get('/',
            summary='Articles index',
            description='Retrieve all articles filled with their author',
            status_code=status.HTTP_200_OK,
            response_model=list[ReadArticleResource])
def index(limit: int | None = Query(25,
                                    description='Maximum size of results set'),
          offset: int = Query(0, description='Starting offset of results set'),
          query: str | None = Query(None, description='Title query'),
          db: Session = Depends(get_db)):
    return article_repository.get_all(db, dict(limit=limit, offset=offset, query=query))


@router.post('/',
             summary='Create article',
             description='Create article in DB',
             status_code=status.HTTP_201_CREATED,
             response_description='Article created',
             response_model=ArticleResource)
def create(request: CreateArticleRequest, db: Session = Depends(get_db)):
    return article_repository.create(db, request.dict())


@router.get('/{id}',
            summary='Get article',
            description='Retrieve a specific article filled with its author',
            status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_404_NOT_FOUND: {'description': 'Article not found'}
            },
            response_model=ReadArticleResource)
def read(id: int = Path(description='Article ID'), db: Session = Depends(get_db)):
    return article_repository.get(db, id)


@router.put('/{id}',
            summary='Update article',
            description='Update an article by overriding all its data with request',
            status_code=status.HTTP_202_ACCEPTED,
            response_description='Article updated',
            responses={
                status.HTTP_404_NOT_FOUND: {'description': 'Article not found'}
            },
            response_model=ArticleResource)
def update(request: CreateArticleRequest,
           id: int = Path(description='Article ID'),
           db: Session = Depends(get_db)):
    return article_repository.update(db, id, request.dict())


@router.delete('/{id}',
               summary='Delete article',
               description='Delete an article by overriding all its data with request',
               status_code=status.HTTP_204_NO_CONTENT,
               response_description='Article deleted',
               responses={
                   status.HTTP_404_NOT_FOUND: {
                       'description': 'Article not found'}
               })
def delete(id: int = Path(description='Article ID'), db: Session = Depends(get_db)):
    article_repository.delete(db, id)
