import os
from json import load
#from updater import check_software_updates
import pygame
import collection

import scenes.headpiece.functions
import scenes.lobby.functions
import scenes.table.functions
import scenes.settings.functions
import scenes.game.functions


def main():
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()

    base_dir = os.path.dirname(os.path.abspath(__file__))

    with open(f'{base_dir}/config/config.json', 'r') as file:
        config = load(file)

    #check_software_updates(config['version'], base_dir)

    with open(f'{base_dir}/config/user.json', 'r') as file:
        config['user'] = load(file)

    if config['user']['full_screen']:
        screen = pygame.display.set_mode(config['mode'], pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode(config['mode'])

    pygame.display.set_caption(config['caption'])
    pygame.display.set_icon(pygame.image.load(f'{base_dir}/icon.ico'))

    clock = pygame.time.Clock()

    tick = 0

    # Headpiece init
    text = scenes.headpiece.functions.init(screen, base_dir, config, 'YariKartoshe4ka')

    # Lobby init
    play_button, table_button, settings_button, caption = scenes.lobby.functions.init(screen, base_dir, config)

    # Table init
    table, back_button = scenes.table.functions.init(screen, base_dir, config)

    # Settings init
    effects_button, full_screen_button, difficulty_button, nick_input = scenes.settings.functions.init(screen, base_dir, config)
    settings_buttons = pygame.sprite.Group()
    settings_buttons.add(effects_button, full_screen_button, difficulty_button)

    # Game init
    bg, plate, score, end, pause = scenes.game.functions.init(screen, base_dir, config, 'Score: 0')
    astrs = pygame.sprite.Group()
    boosts = collection.BoostsGroup()

    while True:
        tick += 1

        if config['scene'] == 'headpiece':
            scenes.headpiece.functions.check_events(config, base_dir)
            scenes.headpiece.functions.update(screen, config, text, tick)

        elif config['scene'] == 'lobby':
            scenes.lobby.functions.check_events(config, base_dir, play_button, table_button, back_button, settings_button, caption)
            scenes.lobby.functions.update(bg, play_button, table_button, settings_button, caption)

        elif config['scene'] == 'table':
            scenes.table.functions.check_events(config, back_button, play_button, table_button, settings_button)
            scenes.table.functions.update(base_dir, bg, table, back_button)

        elif config['scene'] == 'settings':
            scenes.settings.functions.check_events(config, back_button, play_button, table_button, settings_button, effects_button, full_screen_button, difficulty_button, nick_input)
            scenes.settings.functions.update(bg, config, back_button, settings_buttons, nick_input)
            
            if full_screen_button.changed != config['user'][full_screen_button.index]:
                screen = pygame.display.set_mode(config['mode'], pygame.FULLSCREEN * config['user'][full_screen_button.index])
                full_screen_button.changed = config['user'][full_screen_button.index]

        elif config['scene'] == 'game':
            scenes.game.functions.update(screen, config, base_dir, bg, plate, astrs, boosts, score, end, pause, tick)
            scenes.game.functions.check_collides(config, base_dir, astrs, boosts, plate, play_button, table_button, settings_button, table)
            scenes.game.functions.check_events(config, base_dir, plate, astrs, boosts, end, pause, play_button, table_button, settings_button)


        if tick >= config['FPS'] * 10:
            tick = 0

        if config.get('debug'):
            print(f'FPS: {clock.get_fps()}', end='\r')

        pygame.display.update()
        clock.tick(config['FPS'])


if __name__ == '__main__':
    main()
