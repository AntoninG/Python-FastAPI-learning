from fastapi import FastAPI
from enum import Enum

app = FastAPI()


class Entity(str, Enum):
    users = 'users'
    todo_lists = 'todo-lists'


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"},
                 {"item_name": "Baz"}]


@app.get('/')
async def root() -> dict:
    return {'message': 'Root', 'status': 'OK'}


@app.get('/users/me')
async def me() -> dict:
    return {'user_id': 'Incel'}


@app.get('/{entities}/{entity_id}')
async def read_entity(entities: Entity, entity_id: int) -> dict:
    return {'entities': entities, 'id': entity_id}


@app.get('/{entities}')
async def read_entities(entities: Entity, offset: int = 0, limit: int = 1,
                        query: str | None = None) -> list:
    items = fake_items_db[offset: offset + limit]
    if not query:
        return items

    for key, item in enumerate(items):
        if query not in item['item_name']:
            del items[key]

    return items


@app.post('/todo-lists')
async def post_todo_list(todo_list):
    return todo_list
