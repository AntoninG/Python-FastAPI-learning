from fastapi import FastAPI, Path, Query, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html

from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI(
    docs_url=os.getenv('DOCS_URL', '/docs'),
    redoc_url=os.getenv('REDOC_URL', '/redoc')
)
app.mount('/static', StaticFiles(directory='static'), name='static')

inventory: dict = {
    1: {
        'name': "Agrax Earthshade",
        'price': 6.30,
        'brand': 'Citadel GW'
    }
}

class Item(BaseModel):
    name: str
    price: float
    brand: str | None = None


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )


@app.get('/')
async def root() -> dict:
    return {'message': 'Root', 'status': 'OK'}


@app.get('/about')
async def about():
    return {'About': 'Lorem Ispum'}


@app.get('/items/{item_id}')
async def item(
        item_id: int = Path(None, description='Item ID', ge=1),
        query: str = Query(None, description='Search query')) -> dict:
    item = inventory.get(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Item not found')

    if query is None:
        return item

    if query.lower() in item['name'].lower():
        return item


@app.get('/items')
async def items(
        *,  # This accepts any number of keyword arguments
        query: str = Query(None, description='Search query')) -> list:
    if query is None:
        return list(inventory.values())

    result: list = []
    for key in inventory:
        item = inventory[key]
        if query in item['name'].lower():
            result.append(item)

    return result


@app.post('/items')
async def create(item: Item) -> dict:
    max_item_id = max(list(inventory.keys()))
    item_dict = item.dict()
    item_dict.update({'item_id': max_item_id + 1})
    return item_dict


@app.patch('/items/{item_id}')
async def patch(item_id: int, post: Item) -> dict:
    if item_id not in inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Item not found')

    item = inventory[item_id]
    item.update(post.dict())
    return item
