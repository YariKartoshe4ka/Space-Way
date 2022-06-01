from .objects import *


def init(screen, base_dir, config):
    effects = EffectsButton(screen, base_dir, config)
    music = MusicButton(screen, base_dir, config)
    full_screen = FullScreenButton(screen, base_dir, config)
    updates = UpdatesButton(screen, base_dir, config)
    back = SettingsBackButton(screen, base_dir, config)
    nick = NickInput(screen, base_dir, config)

    return effects, music, full_screen, updates, back, nick
