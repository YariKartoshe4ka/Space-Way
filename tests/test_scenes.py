import os
from importlib import import_module

import spaceway
from utils import pygame_env


ROOT_DIR = os.path.dirname(os.path.dirname(__file__)) + '/'


def test_recursive_import():
    exclude_dirs = ('__pycache__',)
    exclude_files = ('__init__.py',)

    for root, dirs, files in os.walk(os.path.dirname(spaceway.scenes.__file__)):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        files[:] = [f for f in files if f.endswith('.py') and f not in exclude_files]

        for imp in dirs:
            obj = root.replace(ROOT_DIR, '').replace('/', '.') + '.' + imp
            assert obj in dir(spaceway.scenes)

        for imp in files:
            obj = root.replace(ROOT_DIR, '').replace('/', '.') + '.' + imp[:-3]
            assert obj in dir(spaceway.scenes)


def test_scenes_functions_availability(pygame_env):
    exclude_dirs = ('__pycache__',)
    functions = ('check_events', 'update')

    for root, dirs, files in os.walk(os.path.dirname(spaceway.scenes.__file__)):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        if not dirs:
            scene = import_module(root.replace(ROOT_DIR, '').replace('/', '.'))

            for function in functions:
                getattr(scene.functions, function)

            scene.init(*pygame_env[:-1])
