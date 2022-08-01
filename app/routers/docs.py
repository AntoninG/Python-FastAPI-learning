"""
Documentation routes
"""

import json
import os
import re
import requests
from bs4 import BeautifulSoup

from fastapi import APIRouter
from fastapi.openapi.docs import get_swagger_ui_html

router = APIRouter()


@router.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title=os.getenv("APP_TITLE", "FastAPI") + " - Swagger UI",
        oauth2_redirect_url="/docs/oauth2-redirect",
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )


@router.get("/about", include_in_schema=False,
            description="About the API", tags=["about"])
def about():
    json_about = json.load(
        open(os.getcwd() + "/static/about.json", encoding="UTF-8")
    )
    json_about["last_pr_at"] = get_last_pr()
    json_about.update(get_scores())

    return json_about


def get_last_pr() -> str | None:
    url_repository = "https://github.com/AntoninG/Python-FastAPI-learning/" \
                     "pulls?q=is%3Apr+is%3Aclosed+is%3Amerged"
    try:
        soup = BeautifulSoup(requests.get(url_repository).text, "html5lib")
        latest_relative_time = soup.find("relative-time")
    except requests.ConnectionError:
        return "error"

    if "datetime" in latest_relative_time:
        return latest_relative_time.attrs["datetime"]

    return None


def get_scores() -> dict:
    result = {"scores": []}

    url_repository = "https://github.com/AntoninG/Python-FastAPI-learning"
    try:
        soup = BeautifulSoup(requests.get(url_repository).text, "html5lib")
    except requests.ConnectionError:
        return result

    img_elements_scores = soup.select('#readme .markdown-body > p img')
    for img in img_elements_scores:
        url_img = "https://github.com" + img.attrs['src']
        try:
            svg_content = requests.get(url_img).text
        except Exception:
            continue

        pattern = re.compile(r'<text[^>]*>([.0-9%]+)</text>', re.I | re.M)
        print(svg_content)
        print(pattern.match(svg_content))

    return result
