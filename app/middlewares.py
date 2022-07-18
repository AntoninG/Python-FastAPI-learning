from fastapi import FastAPI

from .middlewares import print_timings


def load_middlewares(app: FastAPI):
    print_timings.PrintTimingsMiddleware(app)
