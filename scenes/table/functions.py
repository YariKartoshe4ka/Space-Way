import pygame
from sys import exit

from .objects import *


def init(screen, base_dir):
    score = TableScore(screen, base_dir)

    return score


def check_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()


def update(base_dir, bg, score):
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
