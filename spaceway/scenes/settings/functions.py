from sys import exit

import pygame

from .objects import SettingsBackButton


def check_events(config, scene_buttons, effects, full_screen, difficulty, nick):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            scene_buttons.get_by_instance(SettingsBackButton).press()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()

            if scene_buttons.perform_point_collides((x, y)):
                pass

            elif effects._rect.collidepoint((x, y)):
                print('click effects!')
                effects.config['user'][effects.index] = not effects.config['user'][effects.index]
                effects.is_save = True

            elif full_screen._rect.collidepoint((x, y)):
                print('click full screen!')
                full_screen.config['user'][full_screen.index] = not full_screen.config['user'][full_screen.index]
                full_screen.is_save = True

            elif difficulty._rect.collidepoint((x, y)):
                print('click difficulty!')
                difficulty.config['user'][difficulty.index] = (difficulty.config['user'][difficulty.index] + 1) % 4
                difficulty.is_save = True

            if nick._rect.collidepoint((x, y)):
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
            
            nick.save()


def update(bg, config, scene_buttons, settings, nick):
    bg.blit()

    scene_buttons.draw()

    width = 63
    space = 7

    x = (config['mode'][0] - (len(settings) * width + (len(settings) - 1) * space)) // 2

    for button in settings.sprites():
        button.rect.x = x
        button.update()
        button.blit()
        x += width + space

    nick.update()
    nick.blit()
