import pygame
from sys import exit

from .objects import *


pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()


def init(screen, base_dir, config, msg):
    bg = Background(screen, base_dir, 0, 0)
    plate = SpacePlate(screen, base_dir)
    health = Health(screen, base_dir, config)
    score = Score(screen, base_dir, msg)

    return bg, plate, health, score


def check_events(config, base_dir, plate):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        elif event.type == pygame.KEYDOWN and config['scene'] == 'game':
            if event.key == pygame.K_SPACE and plate.rect.top >= plate.screen_rect.top + 50:
                pygame.mixer.music.load(f'{base_dir}/assets/sounds/jump.wav')
                pygame.mixer.music.play()
                plate.is_jump = True


def add_astr(screen, astrs, base_dir, config, tick):
    if tick % 120 == 0:
        astr = Asrteroid(screen, base_dir, config)
        astrs.add(astr)


def update(screen, config, base_dir, bg, plate, astrs, entities, health, score, tick):
    if tick % 2 == 0:
        bg.update()

    bg.blit()

    for astr in astrs.copy():
        if astr.rect.right <= -5:
            astrs.remove(astr)
            pygame.mixer.music.load(f'{base_dir}/assets/sounds/score.wav')
            pygame.mixer.music.play()
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


def check_collides(config, base_dir, astrs, plate, entities, play, table):
    collides = pygame.sprite.spritecollide(plate, astrs, True)

    if collides:
        pygame.mixer.music.load(f'{base_dir}/assets/sounds/bang.wav')
        pygame.mixer.music.play()

        for astr in collides:
            astr.is_bang = True
            config['health'] -= 1

            entities.add(astr)

    elif plate.rect.bottom >= plate.screen_rect.bottom:
        pygame.mixer.music.load(f'{base_dir}/assets/sounds/bang.wav')
        pygame.mixer.music.play()
        plate.is_jump = True
        config['health'] -= 1

    if config['health'] == 0:

        with open(f'{base_dir}/config/score.csv', 'a') as file:
            line = ','.join([str(config['score']), config['nick']]) + '\n'
            file.write(line)

        config['health'] = 3

        plate.reset()
        astrs.empty()
        entities.empty()

        play.to_bottom = True
        table.to_top = True
        config['scene'] = 'lobby'
