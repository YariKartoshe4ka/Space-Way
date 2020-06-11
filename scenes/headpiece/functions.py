import pygame
from sys import exit

from .objects import *


def init(screen, base_dir, config, msg):
    text = Text(screen, base_dir, msg)

    return text


def check_events(config, base_dir):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()


def update(screen, config, text, tick):
    screen.fill((0, 0, 0))

    if tick % 120 == 0:
        config['scene'] = 'lobby'

    if tick % 60 == 0:
        text.msg = 'With love'

    text.update()
    text.blit()