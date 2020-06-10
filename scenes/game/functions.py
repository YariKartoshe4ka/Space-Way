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


def add_astr(screen, astrs, base_dir, config, tick):
    if tick % 120 == 0:
        astr = Asrteroid(screen, base_dir, config)
        astrs.add(astr)


def update(screen, config, bg, plate, astrs, tick):
    if tick % 2 == 0:
        bg.update()

    bg.blit()

    for astr in astrs.copy():
        if astr.rect.right <= -5:
            astrs.remove(astr)

    for astr in astrs.sprites():
        astr.update() 
        astr.blit()

    plate.update()
    plate.blit()


def check_collides(config, astrs, plate):
    if pygame.sprite.spritecollideany(plate, astrs) or plate.rect.bottom >= plate.screen_rect.bottom:
        config['location'] = 'lobby'
