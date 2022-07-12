from fastapi import FastAPI, Depends, HTTPException, status
from . import schemas, models, database
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/articles', status_code=status.HTTP_201_CREATED,
          response_model=schemas.ArticleResource)
def create(request: schemas.Article, db: Session = Depends(get_db)):
    new_article = models.Article(**request.dict())
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article


@app.put('/articles/{id}', status_code=status.HTTP_202_ACCEPTED,
         response_model=schemas.ArticleResource)
def update(id: int, request: schemas.Article, db: Session = Depends(get_db)):
    article_query = db.query(models.Article).filter(models.Article.id == id)
    article = article_query.first()
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    article_query.update(request.dict())
    db.commit()
    db.refresh(article)

    return article


@app.get('/articles', status_code=status.HTTP_200_OK,
         response_model=list[schemas.ArticleResource])
def index(db: Session = Depends(get_db)):
    return db.query(models.Article).all()


@app.get('/articles/{id}', status_code=status.HTTP_200_OK,
         response_model=schemas.ArticleResource)
def read(id: int, db: Session = Depends(get_db)):
    article = db.query(models.Article).filter(models.Article.id == id).first()

    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return article


@app.delete('/articles/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)):
    article = db.query(models.Article) \
        .filter(models.Article.id == id) \
        .delete(synchronize_session=False)

    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    db.commit()
