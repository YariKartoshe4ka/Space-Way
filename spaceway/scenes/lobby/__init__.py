from .objects import *


def init(screen, base_dir, config):
    play = PlayButton(screen, base_dir, config)
    table = TableButton(screen, base_dir, config)
    settings = SettingsButton(screen, base_dir, config)
    caption = Caption(screen, base_dir, config)

    return play, table, settings, caption
