from sys import exit

import pygame

from .objects import SettingsBackButton


def check_events(config, scene_buttons, settings_buttons, nick):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            scene_buttons.get_by_instance(SettingsBackButton).press()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()

            if scene_buttons.perform_point_collides((x, y)):
                pass

            elif settings_buttons.perform_point_collides((x, y)):
                config.save()

            if nick.rect.collidepoint((x, y)):
                nick.enable()
            else:
                nick.disable()

        elif event.type == pygame.KEYDOWN and nick.state > 0:
            nick.add_char(event.unicode)
            config.save()


def update(bg, config, scene_buttons, settings_buttons, nick):
    bg.blit()

    scene_buttons.draw()
    settings_buttons.draw()

    for settings_button in settings_buttons:
        settings_button.blit_hint()

    nick.update()
    nick.blit()
