import importlib
import pkgutil


def load_scenes(package=__package__):
    if isinstance(package, str):
        package = importlib.import_module(package)

    for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
        full_name = package.__name__ + '.' + name
        globals()[full_name] = importlib.import_module(full_name)
        if is_pkg:
            load_scenes(full_name)


load_scenes()
