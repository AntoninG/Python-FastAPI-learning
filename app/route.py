from . import routers
from app.utils.modules import load_modules


def load_routes(app):
    for module in load_modules(routers.__path__, routers.__package__):
        app.include_router(
            module.router,
            prefix=module.prefix if hasattr(module, 'prefix') else '',
            tags=module.tags if hasattr(module, 'tags') else None
        )
