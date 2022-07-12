from fastapi import FastAPI
from . import schemas, models, database

app = FastAPI()

models.Base.metadata.create_all(database.engine)


@app.post('/articles')
def create(article: schemas.Article):
    return article.dict()
