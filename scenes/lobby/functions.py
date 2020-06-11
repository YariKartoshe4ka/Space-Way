import pygame
from sys import exit

from .objects import *


def init(screen, base_dir, config):
    play = PlayButton(screen, base_dir, config)
    table = TableButton(screen, base_dir, config)

    return play, table


def check_events(config, base_dir, play, table):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()

            if play._rect.collidepoint((x, y)):
                print('click play!')
                play.change_scene = True
                play.to_top = True
                table.to_bottom = True

            elif table._rect.collidepoint((x, y)):
                print('click table!')
                play.to_top = True
                table.change_scene = True
                table.to_bottom = True



def update(bg, play, table):
    bg.blit()

    play.update()
    play.blit()

    table.update()
    table.blit()
