from sys import exit

import pygame


def check_events(config, base_dir):
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            exit()


def update(screen, config, text):
    screen.fill((0, 0, 0))

    if config['ns'].tick % (config['FPS'] * 4) == 0:
        config['scene'] = config['sub_scene'] = 'lobby'

    elif config['ns'].tick % (config['FPS'] * 2) == 0:
        text.msg = 'With love'

    text.update()
    text.blit()
