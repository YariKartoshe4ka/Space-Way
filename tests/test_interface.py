import os
from threading import Thread

import pytest
import pygame
from pygame.event import Event

from spaceway import main
from spaceway.updater import check_software_updates

from utils import pygame_emulate_events


@pytest.mark.timeout(20)
def test_updater():
    base_dir = os.path.dirname(os.path.abspath(main.__file__))

    # Test *View* and *Close* buttons
    pygame_emulate_events(
        Thread(target=check_software_updates, args=('0.0.0a', base_dir)),
        [
            (Event(pygame.MOUSEBUTTONDOWN, pos=(75, 177)), 2500),     # Press *View* button
            (Event(pygame.MOUSEBUTTONDOWN, pos=(228, 177)), 1500),    # Press *Close* button
        ]
    )

    # Test if window is closed by exiting
    pygame_emulate_events(
        Thread(target=check_software_updates, args=('0.0.0a', base_dir)),
        [(Event(pygame.QUIT), 2500)]
    )

    # Test if installed version is newer than remote
    check_software_updates('999.0.0', base_dir)
