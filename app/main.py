import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from . import database, middlewares, routes

load_dotenv()
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
    docs_url=os.getenv('DOCS_URL', '/docs'),
    redoc_url=os.getenv('REDOC_URL', '/redoc'),
)
app.mount('/static', StaticFiles(directory='static'), name='static')

# Create DB schemas
database.Base.metadata.create_all(database.engine)

# Routes
routes.load_routes(app)

# Middlewares
middlewares.load_middlewares(app)
