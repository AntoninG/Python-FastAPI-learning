import json
import os
from dotenv import load_dotenv

from fastapi import FastAPI, Path, Query
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html
from pydantic import BaseModel

load_dotenv()
app = FastAPI(
    docs_url=os.getenv('DOCS_URL', '/docs'),
    redoc_url=os.getenv('REDOC_URL', '/redoc')
)
app.mount('/static', StaticFiles(directory='static'), name='static')


class Article(BaseModel):
    title: str
    content: str
    published_at: str | None = None
    metadata: dict | None = {}


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )


@app.get('/', summary='Root', description='Root')
async def index():
    return {'data': {'name': 'AGU', 'message': 'Hello world'}}


@app.get('/about', description='About the API')
async def about():
    return json.load(open(os.getcwd() + '/static/about.json'))


@app.get(
    '/articles/{id}',
    summary='Display a specific article',
    status_code=200
)
async def show(id: int = Path(description="Article ID")):
    return {'data': {'id': id}}


@app.get(
    '/articles/{id}/comments',
    summary='Display a specific article comments',
    status_code=200
)
async def show_comments(id: int = Path(description="Article ID")):
    return {'data': {'comments': list(range(0, id))}}


@app.get('/articles')
async def index(
        limit: int | None = Query(100,
                                  description='Maximum size of results set'),
        offset: int | None = Query(0,
                                   description='Starting offset of results set'),
        query: str | None = Query(None,
                                  description='Query string to filter results set on title and content'),
        published: bool | None = Query(None,
                                       description='Only published or unpublished articles')
):
    articles = list(range(offset, limit))
    for key, item in enumerate(articles):
        status = 'available'
        if published is not None:
            status = 'published' if published is True else 'unpublished'

        articles[key] = {
            'name': query if query is not None else None,
            'status': status
        }
    return articles


@app.post('/articles', status_code=201)
async def create(article: Article):
    return article.dict()
