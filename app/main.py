from pkgutil import iter_modules, get_loader
from fastapi import FastAPI
from . import models, database, routers

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
)

models.Base.metadata.create_all(database.engine)


for importer, name, ispkg in list(iter_modules(routers.__path__)):
    module_package_name = '{0}.{1}'.format(routers.__dict__['__package__'], name)
    module = get_loader(module_package_name).load_module(module_package_name)

    if not hasattr(module, 'router'):
        continue

    app.include_router(module.router,
                       prefix=module.prefix if hasattr(module, 'prefix') else '',
                       tags=module.tags if hasattr(module, 'tags') else None)
