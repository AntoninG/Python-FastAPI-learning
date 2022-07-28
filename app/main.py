"""
App main
"""

import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.utils import database, event, middleware, route

load_dotenv()
app = FastAPI(
    title="News articles",
    description="",
    version="0.0.1",
    terms_of_service=None,
    contact={
        "name": "Antoin Gilette",
        "url": "https://github.com/AntoninG",
        "email": "antonin.guilet-dupont@laposte.net",
    },
    license_info=None,
    docs_url=os.getenv("DOCS_URL", "/docs"),
    redoc_url=os.getenv("REDOC_URL", "/redoc"),
)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Create DB schemas
database.Base.metadata.create_all(database.engine)


# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Routes
route.load_routes(app)

# Middlewares
middleware.load_middlewares(app)

# Events
event.load_events(app)
