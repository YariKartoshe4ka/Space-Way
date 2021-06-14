import os
from json import load

import pygame

from . import scenes, collection, updater
from .config import ConfigManager


def main():
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()

    base_dir = os.path.dirname(os.path.abspath(__file__))

    config = ConfigManager(base_dir)

    updater.check_software_updates(config['version'], base_dir)

    if config['user']['full_screen']:
        screen = pygame.display.set_mode(config['mode'], pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode(config['mode'])

    pygame.display.set_caption(config['caption'])
    pygame.display.set_icon(pygame.image.load(f'{base_dir}/icon.ico'))

    clock = pygame.time.Clock()

    tick = 0

    # Headpiece init
    text = scenes.headpiece.init(screen, base_dir, config)

    # Lobby init
    play_button, table_button, settings_button, caption = scenes.lobby.init(screen, base_dir, config)

    # Table init
    table, table_back_button = scenes.table.init(screen, base_dir, config)

    # Settings init
    effects_button, full_screen_button, difficulty_button, settings_back_button, nick_input = scenes.settings.init(screen, base_dir, config)

    settings_buttons = collection.CenteredButtonsGroup(config['mode'])
    settings_buttons.add(effects_button, full_screen_button, difficulty_button)

    # Game init
    astrs = pygame.sprite.Group()
    boosts = collection.BoostsGroup()

    bg, plate, score, end, pause, resume_button, pause_lobby_button, again_button, end_lobby_button = scenes.game.init(screen, base_dir, config, astrs, boosts, table)

    pause_buttons = collection.CenteredButtonsGroup(config['mode'])
    pause_buttons.add(pause_lobby_button, resume_button)

    end_buttons = collection.CenteredButtonsGroup(config['mode'])
    end_buttons.add(end_lobby_button, again_button)

    # Buttons linking
    scene_buttons = collection.SceneButtonsGroup(config)
    scene_buttons.add(play_button, table_button, settings_button,
                      settings_back_button, table_back_button, resume_button,
                      pause_lobby_button, again_button, end_lobby_button)

    while True:
        tick += 1

        if config['scene'] == 'headpiece':
            scenes.headpiece.functions.check_events(config, base_dir)
            scenes.headpiece.functions.update(screen, config, text, tick)

        elif config['scene'] == 'lobby':
            scenes.lobby.functions.check_events(config, base_dir, scene_buttons, caption)
            scenes.lobby.functions.update(bg, scene_buttons, caption)

        elif config['scene'] == 'table':
            scenes.table.functions.check_events(config, scene_buttons)
            scenes.table.functions.update(base_dir, bg, table, scene_buttons)

        elif config['scene'] == 'settings':
            scenes.settings.functions.check_events(config, scene_buttons, settings_buttons, nick_input)
            scenes.settings.functions.update(bg, config, scene_buttons, settings_buttons, nick_input)
            
            if full_screen_button.changed:
                screen = pygame.display.set_mode(config['mode'], pygame.FULLSCREEN * int(full_screen_button.state))
                full_screen_button.changed = False

        elif config['scene'] == 'game':
            scenes.game.functions.update(screen, config, base_dir, bg, plate, astrs, boosts, score, end, pause, tick, pause_buttons, end_buttons, scene_buttons)
            scenes.game.functions.check_collides(config, base_dir, astrs, boosts, plate, table, end)
            scenes.game.functions.check_events(config, base_dir, plate, astrs, boosts, end, pause, scene_buttons)


        if tick >= config['FPS'] * 10:
            tick = 0

        pygame.display.update()
        clock.tick(config['FPS'])


if __name__ == '__main__':
    main()
