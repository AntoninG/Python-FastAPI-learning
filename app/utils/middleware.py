"""
Loads app middlewares
"""

from fastapi import FastAPI

from app.middlewares.print_timings import PrintTimingsMiddleware


def load_middlewares(app: FastAPI):
    PrintTimingsMiddleware(app)
