import os
import pkgutil

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from . import models, database, routers
from .middlewares import print_timings

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

models.Base.metadata.create_all(database.engine)


def load_modules(path, package):
    modules = []
    for importer, name, ispkg in list(pkgutil.iter_modules(path)):
        module_package_name = '{0}.{1}'.format(package, name)
        module = pkgutil.get_loader(module_package_name) \
            .load_module(module_package_name)

        if ispkg:
            modules += load_modules(module.__path__, module.__package__)
        modules.append(module)

    return modules


# Routes
for module in load_modules(routers.__path__, routers.__package__):
    if not hasattr(module, 'router'):
        continue

    app.include_router(module.router,
                       prefix=module.prefix if hasattr(module,
                                                       'prefix') else '',
                       tags=module.tags if hasattr(module, 'tags') else None)

# Middlewares
print_timings.PrintTimingsMiddleware(app)

