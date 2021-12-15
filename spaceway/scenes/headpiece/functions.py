from sys import exit

import pygame


def check_events(config, base_dir):
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            exit()


def update(screen, config, text, pb):
    text.update()
    text.blit()

    pb.update()
    pb.blit()
