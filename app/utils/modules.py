import pkgutil


def load_modules(path, package):
    modules = []
    for importer, name, ispkg in list(pkgutil.iter_modules(path)):
        module_package_name = '{0}.{1}'.format(package, name)
        module = pkgutil \
            .get_loader(module_package_name) \
            .load_module(module_package_name)

        if ispkg:
            modules += load_modules(module.__path__, module.__package__)
        modules.append(module)

    return modules
