from sys import exit

import pygame


def check_events(config, base_dir):
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            exit()


def update(screen, config, text):
    screen.fill((0, 0, 0))

    if config['namespace'].ticks_headpiece1 + 4000 < pygame.time.get_ticks():
        config['scene'] = config['sub_scene'] = 'lobby'

    elif config['namespace'].ticks_headpiece2 + 2000 < pygame.time.get_ticks():
        text.msg = 'With love'

    text.update()
    text.blit()
