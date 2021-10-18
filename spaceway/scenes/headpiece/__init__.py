from .objects import *


def init(screen, base_dir, config):
    text = Text(screen, base_dir, config)
    pb = ProgressBar(screen, base_dir, config)

    return text, pb
