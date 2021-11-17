import os
from time import time
from random import choices
from string import ascii_letters

import pytest

import pygame
import spaceway


@pytest.fixture(scope='module')
def pygame_env():
    """Creates the basic environment of the game

    Returns:
        screen (pygame.Surface): Screen (surface) obtained via pygame
        base_dir (str): An absolute path to directory where file with the main
            entrypoint is located
        config (spaceway.config.ConfigManager): The configuration object
        clock (pygame.time.Clock): Clock object obtained via pygame
    """
    base_dir = os.path.dirname(os.path.abspath(spaceway.main.__file__))
    config = spaceway.config.ConfigManager(base_dir)
    screen = pygame.display.set_mode(config['mode'])

    config['ns'].dt = 0
    config['ns'].tick = 1
    config['ns'].speed = 2
    config['ns'].score = 0

    clock = pygame.time.Clock()

    return screen, base_dir, config, clock


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
    COLORS = (
        ((0, 57, 255), (255, 46, 222)),
        ((0, 195, 12), (251, 255, 0)),
        ((255, 11, 0), (0, 255, 228))
    )

    s = pygame.Surface(size)
    r = s.get_rect()

    a, b = r.w // 2, r.h // 2

    pygame.draw.rect(s, COLORS[color][0], pygame.Rect(0, 0, a, b))
    pygame.draw.rect(s, COLORS[color][1], pygame.Rect(a, 0, a, b))
    pygame.draw.rect(s, COLORS[color][1], pygame.Rect(0, b, a, b))
    pygame.draw.rect(s, COLORS[color][0], pygame.Rect(a, b, a, b))

    return s


def most_popular_colors(surface, amount=1, exclude=[]):
    """Finds the most common surface colors

    Args:
        surface (pygame.Surface): Surface on which the colors will be searched
        amount (int): Amount of returned colors, defaults to 0
        exclude (list): List of colors that don't need to be counted, defaluts to empty list

    Returns:
        List[Tuple[int, int, int]]: List of the most common colors

    Important:
        Colors are considered without taking into account the alpha channel, i.e. the function
        considers rgba(1, 12, 123, 55) and rgb(1, 12, 123) to be the same, while fully transparent
        pixels (alpha = 0) aren't taken into account in the calculations
    """
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


def rstring(k=5):
    return ''.join(choices(ascii_letters, k=k))
