import os
import socket
from threading import Thread

import pytest
import pygame
from pygame.event import Event

from spaceway import main
from spaceway.updater import check_software_updates

from utils import pygame_emulate_events


BASE_DIR = os.path.dirname(os.path.abspath(main.__file__))


@pygame_emulate_events
def test_updater_buttons():
    return (
        Thread(target=check_software_updates, args=('0.0.0a', BASE_DIR)),
        [
            (Event(pygame.MOUSEBUTTONDOWN, pos=(75, 177)), 2500),     # Press *View* button
            (Event(pygame.MOUSEBUTTONDOWN, pos=(228, 177)), 3000),    # Press *Close* button
        ],
    )


@pygame_emulate_events
def test_updater_exit_button():
    return (
        Thread(target=check_software_updates, args=('0.0.0a', BASE_DIR)),
        [(Event(pygame.QUIT), 2500)]
    )


@pytest.mark.timeout(5)
def test_updater_logic(monkeypatch):
    # Test if installed version is newer than remote
    check_software_updates('999.0.0', BASE_DIR)

    # Test if there is no internet connection
    def guard(*args, **kwargs):
        raise Exception('Network error')

    monkeypatch.setattr(socket, 'socket', guard)
    check_software_updates('0.0.0a', BASE_DIR)
