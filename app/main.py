import os, pkgutil
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from . import models, database, routers

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

# Routes
for importer, name, ispkg in list(pkgutil.iter_modules(routers.__path__)):
    module_package_name = '{0}.{1}'.format(routers.__dict__['__package__'], name)
    module = pkgutil.get_loader(module_package_name)\
        .load_module(module_package_name)

    if not hasattr(module, 'router'):
        continue

    app.include_router(module.router,
                       prefix=module.prefix if hasattr(module, 'prefix') else '',
                       tags=module.tags if hasattr(module, 'tags') else None)
