import pygame
from sys import exit

from .objects import *


def init(screen, base_dir, config, msg):
    bg = Background(screen, base_dir, 0, 0)
    plate = SpacePlate(screen, base_dir)
    health = Health(screen, base_dir, config)
    score = Score(screen, base_dir, msg)

    return bg, plate, health, score


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


def update(screen, config, bg, plate, astrs, entities, health, score, tick):
    if tick % 2 == 0:
        bg.update()

    bg.blit()

    for astr in astrs.copy():
        if astr.rect.right <= -5:
            astrs.remove(astr)
            config['score'] += 1

    for astr in astrs.sprites():
        astr.update() 
        astr.blit()

    for entity in entities.sprites():
        if entity.update():
            entities.remove(entity)
        else:
            entity.blit()

    health.update()
    health.blit()

    score.msg = f"score: {config['score']}"
    score.update()
    score.blit()

    plate.update()
    plate.blit()


def check_collides(config, astrs, plate, entities):
    astrs = pygame.sprite.spritecollide(plate, astrs, True)

    if astrs:
        for astr in astrs:
            astr.is_bang = True
            config['health'] -= 1

            entities.add(astr)

    elif plate.rect.bottom >= plate.screen_rect.bottom:
        plate.is_jump = True
        config['health'] -= 1

    if config['health'] == 0:
        config['location'] = 'lobby'
