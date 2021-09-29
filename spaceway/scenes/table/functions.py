from sys import exit

import pygame

from .objects import TableBackButton


def check_events(config, scene_buttons):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            scene_buttons.get_by_instance(TableBackButton).press()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()

            scene_buttons.perform_point_collides((x, y))


def update(base_dir, bg, table, scene_buttons):
    bg.blit()

    table.update()
    table.blit()

    scene_buttons.draw()
