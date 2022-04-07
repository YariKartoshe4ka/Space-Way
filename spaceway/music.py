""" File with some objects for easier music (sounds) management """

from enum import Enum, auto

import pygame


class SoundGroup(Enum):
    """Enumeration object to determine the type of sound
    """

    EFFECT = auto()   # As a rule, short-term sound
    SOUND = auto()    # A long sound playing in the background


class MusicManager:
    """Music manager - object for easier music configuration. Creates sound
    objects. all sounds belong to a certain imaginary group to determine
    common settings (such as volume)

    Args:
        sounds (Dict[str, Tuple[str, spaceway.music.Channel]]): Dict with
            description of music files (key - sound name, value - file path
            and sound group)
    """

    def __init__(self, sounds):
        """Initializing of MusicManager
        """
        self.__sounds = {}

        for name in sounds:
            path, group = sounds[name]
            self.__sounds[name] = (pygame.mixer.Sound(path), group)

    def get(self, name):
        """Get sound object for its further usage

        Args:
            name (str): Name of the sound

        Returns:
            pygame.mixer.Sound: Sound object
        """
        return self.__sounds[name][0]

    def set_volume(self, volume, group) -> None:
        """Set a specific volume for all sounds of this group

        Args:
            volume (float): Float number in range from 0 to 1
            group (SoundGroup): The group of sounds for which this volume
                should be set
        """
        for name in self.__sounds:
            sound, _group = self.__sounds[name]

            if _group == group:
                sound.set_volume(volume)
