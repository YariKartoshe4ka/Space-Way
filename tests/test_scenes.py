import os
from importlib import import_module
from threading import Thread

import pygame
from pygame.event import Event

import spaceway
from utils import pygame_env, pygame_emulate_events


ROOT_DIR = os.path.dirname(os.path.dirname(spaceway.__file__)) + '/'


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


@pygame_emulate_events
def test_scene_headpiece_quit_by_escape():
    return (
        Thread(target=spaceway.main.main),
        [(Event(pygame.KEYDOWN, key=pygame.K_ESCAPE), 2000)]
    )


@pygame_emulate_events
def test_scene_headpiece_wait_till_lobby():
    return (
        Thread(target=spaceway.main.main),
        [(Event(pygame.KEYDOWN, key=pygame.K_ESCAPE), 4000)]
    )


@pygame_emulate_events
def test_debug_modules():
    return (
        Thread(target=spaceway.main.main),
        [
            (Event(pygame.KEYDOWN, key=pygame.KMOD_LCTRL, mod=pygame.KMOD_LCTRL), 2000),
            (Event(pygame.KEYDOWN, key=pygame.K_s, scancode=22, pressed=True), 500),
            (Event(pygame.KEYDOWN, key=pygame.K_h, scancode=11, pressed=True), 500),
            (Event(pygame.KEYDOWN, key=pygame.K_ESCAPE), 2000)
        ]
    )


@pygame_emulate_events
def test_scenes_complexly():
    return (
        Thread(target=spaceway.main.main),
        [

            (Event(pygame.MOUSEBUTTONDOWN, pos=(37, 414)), 4000),          # Press *table* button
            (Event(pygame.MOUSEBUTTONDOWN, pos=(37, 414)), 2000),          # Press *back* button
            (Event(pygame.MOUSEBUTTONDOWN, pos=(664, 414)), 2000),         # Press *settings* button
            (Event(pygame.MOUSEBUTTONDOWN, pos=(37, 414)), 2000),          # Press *back* button
            *((Event(pygame.MOUSEBUTTONDOWN, pos=(100, 100)), 700),) * 3,  # Press background 3 times
            (Event(pygame.MOUSEBUTTONDOWN, pos=(350, 225)), 2000),         # Press *play* button
            (Event(pygame.KEYDOWN, key=pygame.K_SPACE), 900),              # Press *SPACE* key
            (Event(pygame.KEYDOWN, key=pygame.K_SPACE), 700),              # Press *SPACE* key
            (Event(pygame.KEYDOWN, key=pygame.K_ESCAPE), 100),             # Press *ESC* key
            (Event(pygame.KEYDOWN, key=pygame.K_ESCAPE), 500),             # Press *ESC* key
            (Event(pygame.KEYDOWN, key=pygame.K_ESCAPE), 100),             # Press *ESC* key
            (Event(pygame.MOUSEBUTTONDOWN, pos=(385, 225)), 500),          # Press *resume* button
            (Event(pygame.KEYDOWN, key=pygame.K_ESCAPE), 100),             # Press *ESC* key
            (Event(pygame.MOUSEBUTTONDOWN, pos=(315, 225)), 500),          # Press *lobby* button
            (Event(pygame.QUIT), 2000)
        ]
    )
