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
                print('click nick!')
                nick.is_enable = True
            else:
                nick.is_enable = False

        elif event.type == pygame.KEYDOWN and nick.is_enable:
            if event.key == pygame.K_BACKSPACE:
                nick.config['user']['nick'] = nick.config['user']['nick'][:len(nick.config['user']['nick']) - 1]
            elif event.key == pygame.K_RETURN:
                nick.is_enable = False
            elif event.unicode.encode('ascii', errors='ignore') != b'':
                nick.config['user']['nick'] += event.unicode

            config.save()


def update(bg, config, scene_buttons, settings_buttons, nick):
    bg.blit()

    scene_buttons.draw()
    settings_buttons.draw()

    nick.update()
    nick.blit()
