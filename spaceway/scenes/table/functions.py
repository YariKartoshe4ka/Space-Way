from sys import exit

import pygame

from .objects import *


def init(screen, base_dir, config):
    score = TableScore(screen, base_dir)
    back = BackButton(screen, base_dir, config)

    return score, back


def check_events(config, back, play, table, settings): 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            back.change_scene = True
            back.to_bottom = True
            play.to_bottom = True
            table.to_top = True
            settings.to_top = True

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()

            if back._rect.collidepoint((x, y)):
                print('click back!')
                back.change_scene = True
                back.to_bottom = True
                play.to_bottom = True
                table.to_top = True
                settings.to_top = True


def update(base_dir, bg, score, back):
    bg.blit()

    score.update()
    score.blit()

    back.update()
    back.blit()
