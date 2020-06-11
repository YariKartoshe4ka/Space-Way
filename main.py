import os
from json import load
import pygame

import scenes.headpiece.functions
import scenes.lobby.functions
import scenes.table.functions
import scenes.game.functions


def main():
    pygame.init()

    base_dir = os.path.dirname(os.path.abspath(__file__))

    with open(f'{base_dir}/config/config.json', 'r') as file:
        config = load(file)

    with open(f'{base_dir}/config/user.json', 'r') as file:
        config['user'] = load(file)

    screen = pygame.display.set_mode(config['mode'])
    pygame.display.set_caption(config['caption'])

    clock = pygame.time.Clock()

    tick = 0

    # Headpiece init
    text = scenes.headpiece.functions.init(screen, base_dir, config, 'YariKartoshe4ka')

    # Lobby init
    play_button, table_button = scenes.lobby.functions.init(screen, base_dir, config)

    # Table init
    table, back_button = scenes.table.functions.init(screen, base_dir, config)

    # Game init
    bg, plate, health, score = scenes.game.functions.init(screen, base_dir, config, 'Score: 0')
    entities = pygame.sprite.Group()
    astrs = pygame.sprite.Group()


    while True:
        tick += 1

        if config['scene'] == 'headpiece':
            scenes.headpiece.functions.check_events(config, base_dir)
            scenes.headpiece.functions.update(screen, config, text, tick)

        elif config['scene'] == 'lobby':
            scenes.lobby.functions.check_events(config, base_dir, play_button, table_button, back_button)
            scenes.lobby.functions.update(bg, play_button, table_button)

        elif config['scene'] == 'table':
            scenes.table.functions.check_events(back_button, play_button, table_button)
            scenes.table.functions.update(base_dir, bg, table, back_button, play_button)

        elif config['scene'] == 'game':
            scenes.game.functions.update(screen, config, base_dir, bg, plate, astrs, entities, health, score, tick)
            scenes.game.functions.check_collides(config, base_dir, astrs, plate, entities, play_button, table_button)
            scenes.game.functions.add_astr(screen, astrs, base_dir, config, tick)
            scenes.game.functions.check_events(config, base_dir, plate)


        if tick >= config['FPS'] * 4:
            tick = 0

        pygame.display.update()
        clock.tick(config['FPS'])


if __name__ == '__main__':
    main()