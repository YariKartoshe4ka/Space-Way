""" File with some objects for easier music (sounds) management """

from enum import Enum, auto

import pygame


class SoundType(Enum):
    """Enumeration object to determine the type of sound
    """

    EFFECT = auto()   # As a rule, short-term sound
    SOUND = auto()    # A long sound playing in the background


class MusicManager:
    """Music manager - object for easier music configuration

    Args:
        sounds (Dcit[str, Tuple[str, SoundType]]): Dict with description of
            music files (key - sound name, value - file path and sound type)
    """

    def __init__(self, sounds):
        """Initializing of MusicManager
        """
        self.__sounds = {}

        for name in sounds:
            path, Type = sounds[name]
            self.__sounds[name] = (pygame.mixer.Sound(path), Type)

    def get(self, name):
        """Gets sound object for its further usage

        Args:
            name (str): Name of the sound

        Returns:
            pygame.mixer.Sound: Sound object
        """
        return self.__sounds[name][0]

    def set_volume(self, volume, Type) -> None:
        """Sets a specific volume for all sounds of this type

        Args:
            volume (float): Float number in range from 0 to 1
            Type (SoundType): The type of sounds for which this volume should
                be set
        """
        for name in self.__sounds:
            sound, _Type = self.__sounds[name]

            if _Type == Type:
                sound.set_volume(volume)
