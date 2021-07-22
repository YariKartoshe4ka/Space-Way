""" Module responsible for the Space Way updates """

import os
from webbrowser import open

import pygame
from packaging.version import parse
from requests import get


def dialog(base_dir) -> None:
    """ Creator of information dialog """

    # Setup screen
    MODE = (WIDTH, HEIGHT) = (300, 200)
    screen = pygame.display.set_mode(MODE)
    screen_rect = screen.get_rect()
    pygame.display.set_caption('Space Way Update')

    clock = pygame.time.Clock()

    # Setup fonts
    font = pygame.font.Font(f'{base_dir}/assets/fonts/pixeboy.ttf', 28)

    # Setup other drawable objects
    bg = pygame.image.load(f'{base_dir}/assets/updater/background.bmp')
    bg_rect = bg.get_rect()

    title_top = font.render('New version', True, (0, 255, 255))
    title_top_rect = title_top.get_rect()
    title_top_rect.center = screen_rect.center
    title_top_rect.top -= 20

    title_bottom = font.render('available', True, (0, 255, 255))
    title_bottom_rect = title_bottom.get_rect()
    title_bottom_rect.center = screen_rect.center

    view_text = font.render('View', True, (0, 255, 0))
    view_text_rect = view_text.get_rect()
    view_text_rect.centerx = WIDTH // 4
    view_text_rect.bottom = screen_rect.bottom - 15

    close_text = font.render('Close', True, (255, 0, 0))
    close_text_rect = close_text.get_rect()
    close_text_rect.centerx = WIDTH - WIDTH // 4
    close_text_rect.bottom = screen_rect.bottom - 15

    while True:
        for event in pygame.event.get():
            # Checks if user close window
            if event.type == pygame.QUIT:
                return

            # Checks if user press mouse button
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = (x, y) = pygame.mouse.get_pos()

                # If he pressed `View`
                if view_text_rect.collidepoint(pos):
                    open('https://github.com/YariKartoshe4ka/Space-Way/releases/latest')

                # If he pressed `Close`
                elif close_text_rect.collidepoint(pos):
                    return

        # Blitting objects
        screen.blit(bg, bg_rect)
        screen.blit(title_top, title_top_rect)
        screen.blit(title_bottom, title_bottom_rect)
        screen.blit(view_text, view_text_rect)
        screen.blit(close_text, close_text_rect)

        # Update screen
        pygame.display.update()

        # Sync FPS
        clock.tick(30)


def check_software_updates(version, base_dir) -> None:
    """ Сhecks for available updates. If there are any, opens an information dialog """

    # Get remote vesrion of `config.json` if network connection available
    try:
        r = get('https://raw.githubusercontent.com/YariKartoshe4ka/Space-Way/master/spaceway/config/config.json')
    except:
        return

    # Get value of `version` in remote version of `config.json`
    remote_version = r.json().get('version', '0.0.0')

    # Open information dialog if new version available
    if parse(version) < parse(remote_version):
        dialog(base_dir)
