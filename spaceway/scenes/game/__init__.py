from .objects import *


def init(screen, base_dir, config):
    config['ns'].speed = 2
    config['ns'].current_time = 0
    config['ns'].score = 0

    bg = Background(screen, base_dir, config)
    plate = SpacePlate(screen, base_dir, config)
    score = Score(screen, base_dir, 'Score: 0')
    end = EndCaption(screen, base_dir, config)
    pause = PauseCaption(screen, base_dir, config)

    resume_button = ResumeButton(screen, base_dir, config)
    pause_lobby_button = PauseLobbyButton(screen, base_dir, config)

    again_button = AgainButton(screen, base_dir, config)
    end_lobby_button = EndLobbyButton(screen, base_dir, config)

    pause_button = PauseButton(screen, base_dir, config)

    return bg, plate, score, end, pause, resume_button, \
        pause_lobby_button, again_button, end_lobby_button, pause_button
