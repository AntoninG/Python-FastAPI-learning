from fastapi import FastAPI, Path, Query, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

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
    brand: str = None


@app.get('/')
async def root() -> dict:
    return {'message': 'Root', 'status': 'OK'}


@app.get('/about')
async def about():
    return {'About': 'Lorem Ispum'}


@app.get('/items/{item_id}')
async def item(
        item_id: int = Path(None, description='Item ID', ge=1),
        query: str = Query(None, description='Search query')) -> dict | None:
    item = inventory.get(item_id)
    if query is None:
        return item

    if query.lower() in item['name'].lower():
        return item

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='Item not found')


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
