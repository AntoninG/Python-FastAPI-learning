"""
Module to define function to manipulate internal modules
"""

import pkgutil


def load_modules(path, package):
    modules = []
    # pylint: disable=unused-variable
    for importer, name, ispkg in list(pkgutil.iter_modules(path)):
        module_package_name = f'{package}.{name}'
        module = pkgutil \
            .get_loader(module_package_name) \
            .load_module(module_package_name)

        if ispkg:
            modules += load_modules(module.__path__, module.__package__)
        modules.append(module)

    return modules
