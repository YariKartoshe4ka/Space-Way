import pygame
from sys import exit

from .objects import *


def init(screen, base_dir):
    bg = Background(screen, base_dir, 0, 0)
    plate = SpacePlate(screen, base_dir)

    return bg, plate


def check_events(config, plate):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        elif event.type == pygame.KEYDOWN and config['location'] == 'game':
            if event.key == pygame.K_SPACE and plate.rect.top >= plate.screen_rect.top + 50:
                plate.is_jump = True


def update(screen, bg, plate, tick):
    if tick % 2 == 0:
        bg.update()

    bg.blit()

    plate.update()
    plate.blit()
