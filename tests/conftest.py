import os

import pygame
import pytest

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
