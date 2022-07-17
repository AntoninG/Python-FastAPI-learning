from fastapi import FastAPI, Depends, HTTPException, status
from . import models, database
from .schemas import requests, resources
from .hashing import Hash
from sqlalchemy.orm import Session

app = FastAPI(
    title="News articles",
    description='',
    version="0.0.1",
    terms_of_service=None,
    contact={
        "name": "Antoin Gilette",
        "url": "https://github.com/AntoninG",
        "email": "antonin.guilet-dupont@laposte.net",
    },
    license_info=None,
)

models.Base.metadata.create_all(database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/articles', tags=['articles'], status_code=status.HTTP_200_OK,
         response_model=list[resources.ReadArticleResource])
def index(db: Session = Depends(get_db)):
    return db.query(models.Article).all()


@app.post('/articles', tags=['articles'], status_code=status.HTTP_201_CREATED,
          response_model=resources.ArticleResource)
def create(request: requests.CreateArticleRequest,
           db: Session = Depends(get_db)):
    article_dict = request.dict()
    article_dict.update({'user_id': 1})
    new_article = models.Article(**article_dict)

    db.add(new_article)
    db.commit()
    db.refresh(new_article)

    return new_article


@app.get('/articles/{id}', tags=['articles'], status_code=status.HTTP_200_OK,
         response_model=resources.ReadArticleResource)
def read(id: int, db: Session = Depends(get_db)):
    article = db.query(models.Article).filter(models.Article.id == id).first()

    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return article


@app.put('/articles/{id}', tags=['articles'],
         status_code=status.HTTP_202_ACCEPTED,
         response_model=resources.ArticleResource)
def update(id: int, request: requests.CreateArticleRequest,
           db: Session = Depends(get_db)):
    article_query = db.query(models.Article).filter(models.Article.id == id)
    article = article_query.first()
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    article_query.update(request.dict())
    db.commit()
    db.refresh(article)

    return article


@app.delete('/articles/{id}', tags=['articles'],
            status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)):
    article = db.query(models.Article) \
        .filter(models.Article.id == id) \
        .delete(synchronize_session=False)

    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    db.commit()


@app.post('/users', tags=['users'], status_code=status.HTTP_201_CREATED,
          response_model=resources.UserResource)
def create_user(request: requests.CreateUserRequest,
                db: Session = Depends(get_db)):
    request_dict = request.dict()

    request_dict['password'] = Hash.bcrypt(request.password)

    user = models.User(**request_dict)
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@app.get('/users/{id}', tags=['users'], status_code=status.HTTP_200_OK, response_model=resources.ReadUserResource)
def read_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return user


@app.post('/users/{id}/verify-password', tags=['users'],
          status_code=status.HTTP_200_OK,
          response_model=resources.PasswordVerifyResource)
def verify_password(id: int, request: requests.PasswordVerifyRequest,
                    db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return {'password': Hash.verify(request.password, user.password)}
