from .objects import *
from .functions import defeat


def init(screen, base_dir, config, astrs, boosts):
    config['ns'].speed = 2
    config['ns'].score = 0

    bg = Background(screen, base_dir, config)
    plate = SpacePlate(screen, base_dir, config)
    score = Score(screen, base_dir, 'Score: 0')
    end = EndCaption(screen, base_dir, config)
    pause = PauseCaption(screen, base_dir, config)

    resume_button = ResumeButton(screen, base_dir, config)
    pause_lobby_button = PauseLobbyButton(screen, base_dir, config, defeat,
                                          plate, astrs, boosts, end, config, base_dir)

    again_button = AgainButton(screen, base_dir, config)
    end_lobby_button = EndLobbyButton(screen, base_dir, config)

    return bg, plate, score, end, pause, resume_button, \
        pause_lobby_button, again_button, end_lobby_button
