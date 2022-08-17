from importlib import import_module, reload
from random import choices
from string import ascii_letters
from time import sleep, time
from types import ModuleType

import pygame
import pytest

import spaceway


def pygame_loop(pygame_env, duration):
    """Creates a decorator for quickly creating a game loop

    Args:
        pygame_env (tuple): The environment of the game created with :pygame_env:`tests.pygame_env`
        duration (float): Loop duration (in seconds)

    Returns:
        callable: Customized decorator

    Example:
        .. code:: python

        @pygame_loop(pygame_env, 5)
        def test_loop():
            button.update()
            ...
            button.blit()
            ...
            print('Go to another iteration!')

        >>> Go to another iteration!
        >>> Go to another iteration!
        ...
        >>> Go to another iteration!
        >>>
    """
    def decorator(func):
        screen, base_dir, config, clock = pygame_env
        config['ns'].dt = 1000 / config['FPS'] * 0.03
        end = time() + duration

        while end > time():
            pygame.event.get()
            screen.fill((0, 0, 0))

            func()

            pygame.display.update()
            config['dt'] = clock.tick(config['FPS']) * 0.03
            config['ns'].tick += 1

    return decorator


def pygame_surface(size, color=0):
    """Creates a colored test surface

    Args:
        size (Tuple[int, int]): Size (width and height) of surface
        color (int): Index of specific color, defaults to 0

    Returns:
        pygame.Surface: Colored surface (grid 2x2 colored in two colors, in a staggered order)
    """
    colors = (
        ((0, 57, 255), (255, 46, 222)),
        ((0, 195, 12), (251, 255, 0)),
        ((255, 11, 0), (0, 255, 228))
    )

    s = pygame.Surface(size)
    r = s.get_rect()

    a, b = r.w // 2, r.h // 2

    pygame.draw.rect(s, colors[color][0], pygame.Rect(0, 0, a, b))
    pygame.draw.rect(s, colors[color][1], pygame.Rect(a, 0, a, b))
    pygame.draw.rect(s, colors[color][1], pygame.Rect(0, b, a, b))
    pygame.draw.rect(s, colors[color][0], pygame.Rect(a, b, a, b))

    return s


def most_popular_colors(surface, amount=1, exclude=None):
    """Finds the most common surface colors

    Args:
        surface (pygame.Surface): Surface on which the colors will be searched
        amount (int): Amount of returned colors, defaults to 0
        exclude (Optional[list]): List of colors that don't need to be counted, defaluts to empty list

    Returns:
        List[Tuple[int, int, int]]: List of the most common colors

    Important:
        Colors are considered without taking into account the alpha channel, i.e. the function
        considers rgba(1, 12, 123, 55) and rgb(1, 12, 123) to be the same, while fully transparent
        pixels (alpha = 0) aren't taken into account in the calculations
    """
    if not exclude:
        exclude = []

    width, height = surface.get_size()
    colors = {}

    for x in range(0, width):
        for y in range(0, height):
            pixel = surface.get_at((x, y))

            if len(pixel) == 3 and pixel not in exclude:
                colors[pixel] = colors.get(pixel, 0)
            elif (len(pixel) == 4 and pixel[3] != 0) and pixel[:3] not in exclude:
                colors[pixel[:3]] = colors.get(pixel[:3], 0) + 1

    sorted_colors = sorted(colors, key=lambda x: colors[x], reverse=True)
    return sorted_colors[:amount]


def reload_spaceway():
    """Reloads :module:`spaceway` module and all submodules by DFS strategy
    """
    visited = set()

    def dfs(module):
        if module in visited:
            return

        visited.add(module)

        for obj in dir(module):
            obj = getattr(module, obj)

            if isinstance(obj, ModuleType) and obj.__package__.startswith('spaceway'):
                dfs(obj)
            elif hasattr(obj, '__module__') and obj.__module__.startswith('spaceway'):
                dfs(import_module(obj.__module__))

        reload(module)

    dfs(spaceway)


def pygame_emulate_events(func):
    """Decorator, which emulates pygame events (keyboard presses, mouse clicks and other)
    for testing program interface. Test funciton must return args in list accordingly
    specified below

    Args:
        thread (threading.Thread): Thread which targeted to the entry point of the program
        events (List[Tuple[pygame.event.Event, int]]): List of tuples, where the first object
            is emulated event, and the second is interval after previous event (milliseconds)

    Raises:
        Exception: if thread is finished before emulating all events or
            if after thread finishing there are still some events

    Example:
        .. code:: python

        def test():
            return (
                Thread(target=spaceway.main.main),
                [
                    (Event(pygame.KEYDOWN, key=pygame.K_ESCAPE), 2000),
                ]
            )
    """
    thread, events = func()

    @pytest.mark.filterwarnings('ignore::pytest.PytestUnhandledThreadExceptionWarning')
    def decorator(monkeypatch):
        reload_spaceway()

        pos = (0, 0)
        monkeypatch.setattr(pygame.mouse, 'get_pos', lambda: pos)

        pressed = pygame.key.get_pressed()
        monkeypatch.setattr(pygame.key, 'get_pressed', lambda: pressed)

        mods = 0
        monkeypatch.setattr(pygame.key, 'get_mods', lambda: mods)

        thread.daemon = True
        thread.start()
        events.reverse()

        while thread.is_alive():
            if len(events) == 0:
                # Waiting for the thread to finish
                sleep(1)

                if thread.is_alive():
                    thread.join(0)
                    reload_spaceway()

                    raise Exception('Thread is alive but there are no events!')

                break

            event, wait = events.pop()
            sleep(wait / 1000)

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos

            elif event.type == pygame.KEYDOWN:
                if hasattr(event, 'mod'):
                    mods |= event.mod

                if hasattr(event, 'pressed'):
                    scancodes = list(pressed)
                    scancodes[event.scancode] = event.pressed
                    pressed = pygame.key.ScancodeWrapper(scancodes)

            pygame.event.post(event)

        reload_spaceway()

        if len(events):
            raise Exception('Thread was finished, but some events ramain!')

    return decorator


def rstring(k=5):
    return ''.join(choices(ascii_letters, k=k))
