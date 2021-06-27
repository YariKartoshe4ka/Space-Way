from sys import exit

import pygame


def check_events(config, base_dir, scene_buttons, caption):
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()

            if not scene_buttons.perform_point_collides((x, y)):
                if config['user']['color'] >= 2:
                    config['user']['color'] = 0
                else:
                    config['user']['color'] += 1

                config.save()


def update(bg, scene_buttons, caption):
    bg.blit()

    scene_buttons.draw()

    caption.blit()
