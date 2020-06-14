import pygame
from sys import exit

from .objects import *


pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()


def init(screen, base_dir, config, msg):
    bg = Background(screen, base_dir, 0, 0)
    plate = SpacePlate(screen, base_dir, config)
    health = Health(screen, base_dir, config)
    score = Score(screen, base_dir, msg)

    return bg, plate, health, score


def check_events(config, base_dir, plate):
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            exit()

        elif event.type == pygame.KEYDOWN and config['scene'] == 'game':
            if event.key == pygame.K_SPACE and plate.rect.top >= plate.screen_rect.top + 50:
                if config['user']['effects'] and plate.jump == 10:
                    plate.jump_sound.stop()
                    plate.jump_sound.play()
                plate.is_jump = True


def update(screen, config, base_dir, bg, plate, astrs, entities, health, score, tick):
    if tick % 2 == 0:
        bg.update()

    bg.blit()

    if tick % 180 == 0:
        config['speed'] += 1

    if tick % 90 == 0:
        astr = Asrteroid(screen, base_dir, config)
        astrs.add(astr)

    for astr in astrs.copy():
        if astr.rect.right <= -5:
            astrs.remove(astr)
            if config['user']['effects']:
                plate.score_sound.stop()
                plate.score_sound.play()
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


def check_collides(config, base_dir, astrs, plate, entities, play, table, settings):
    collides = pygame.sprite.spritecollide(plate, astrs, True)

    if collides:
        for astr in collides:
            plate.bang_sound.stop()
            plate.bang_sound.play()
            astr.is_bang = True
            config['health'] -= 1

            entities.add(astr)

    elif plate.rect.bottom >= plate.screen_rect.bottom:
        if config['user']['effects']:
            plate.bang_sound.stop()
            plate.bang_sound.play()
        plate.is_jump = True
        config['health'] -= 1

    if config['health'] == 0:

        with open(f'{base_dir}/config/score.csv', 'a') as file:
            line = ','.join([str(config['score']), config['user']['nick']]) + '\n'
            file.write(line)

        config['health'] = 3

        plate.reset()
        astrs.empty()
        entities.empty()

        play.to_bottom = True
        table.to_top = True
        settings.to_top = True
        config['scene'] = 'lobby'
