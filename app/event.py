"""
Loads app events
"""

from fastapi import FastAPI

from app.events import on_shutdown_events, on_startup_events


def load_events(app: FastAPI):
    app.add_event_handler('startup', on_startup_events.startup_events)
    app.add_event_handler('shutdown', on_shutdown_events.shutdown_print)
