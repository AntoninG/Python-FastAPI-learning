import json
import os
from fastapi import APIRouter
from fastapi.openapi.docs import get_swagger_ui_html

router = APIRouter()


@router.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url='/openapi.json',
        title=os.getenv('APP_TITLE', 'FastAPI') + " - Swagger UI",
        oauth2_redirect_url="/docs/oauth2-redirect",
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )


@router.get('/about', include_in_schema=False,
            description='About the API', tags=['about'])
async def about():
    return json.load(open(os.getcwd() + '/static/about.json'))
