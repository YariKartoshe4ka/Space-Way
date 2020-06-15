import pygame
from sys import exit

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

    with open(f'{base_dir}/config/score.csv', 'r') as file:
        data = file.read().split('\n')

    msg = []

    data = sorted(list(map(lambda x: [int(x.split(',')[0]), x.split(',')[1]], data[1:len(data) - 1])))
    data.reverse()

    for i in data[:5]:
        msg.append(f'{i[0]} : {i[1]}')


    msg.insert(0, 'Score table')

    score.msg = msg
    score.update()
    score.blit()

    back.update()
    back.blit()
