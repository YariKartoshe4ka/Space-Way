from sys import exit

import pygame


def check_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            exit()


def update(text, pb):
    text.update()
    text.blit()

    pb.update()
    pb.blit()
