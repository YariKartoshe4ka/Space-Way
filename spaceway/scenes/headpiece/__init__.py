from .objects import *


def init(screen, base_dir, config):
    config['namespace'].ticks_headpiece1 = \
        config['namespace'].ticks_headpiece2 = pygame.time.get_ticks()

    text = Text(screen, base_dir, 'YariKartoshe4ka')

    return text
