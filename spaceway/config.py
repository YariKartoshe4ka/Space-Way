""" File with some objects for easier configuration management """

import os
from shutil import copyfile
from json import load, dump

from appdirs import user_config_dir


class Namespace:
    """ Stores variables that do not need to be imported or exported
        Since `ConfigManager` is passed everywhere, it allows you to
        safely exchange variables from different functions and even
        scenes """
    pass


class ConfigManager(dict):
    """ Configuration manager. Inherited from `dict` class and can be
        used as default dictionary. Different configuration files are
        mounted to different points of dictionary, e.g.:

            config.json -> `root dictionary`
            user.json -> 'user'
            score.csv -> 'score_list'

        Manager can use original configurations (which come with the
        package) or user configurations. Use original configurations
        for debugging (they are easier to edit) and do not use them
        for release (because with update of package they will be changed)
        and user progress will not be saved. Use user configurations for
        release, because if they are created they will not be changed
        to new ones """

    # Set `True` to use configurations in user directory, or `False` for package directory
    USE_USER_CONFIGS = True

    def __init__(self, base_dir) -> None:
        """ Initializing of ConfigManager """

        # Setting BASE_DIR const for the further use
        self.BASE_DIR = base_dir

        # Defining of original (package directory) paths to configurations
        self.__ORIGINAL_PATH_USER_CONFIG = f'{base_dir}/config/user.json'
        self.__ORIGINAL_PATH_SCORE_CONFIG = f'{base_dir}/config/score.csv'

        # Defining of user (user directory) paths to configurations
        self.PATH_MAIN_CONFIG = f'{base_dir}/config/config.json'
        self.PATH_USER_CONFIG = f"{user_config_dir('Space Way', False)}/user.json"
        self.PATH_SCORE_CONFIG = f"{user_config_dir('Space Way', False)}/score.csv"

        # Checking if configurations exists
        self.__check_configs()

        # Loading all configurations
        self.__load()

    def __check_configs(self) -> None:
        """ Сhecks whether the configurations have been created and copies
            them to the user's directory if not (if USE_USER_CONFIGS = `True`)
            Replacing user configuration paths with original configuration
            paths (if USE_USER_CONFIGS = `False`) """

        # Checking whether configurations were created and copying its to
        # user configurations directory if not
        if self.USE_USER_CONFIGS:
            if not os.path.exists(self.PATH_USER_CONFIG):
                os.makedirs(os.path.dirname(self.PATH_USER_CONFIG), exist_ok=True)
                copyfile(self.__ORIGINAL_PATH_USER_CONFIG, self.PATH_USER_CONFIG)

            if not os.path.exists(self.PATH_SCORE_CONFIG):
                os.makedirs(os.path.dirname(self.PATH_SCORE_CONFIG), exist_ok=True)
                copyfile(self.__ORIGINAL_PATH_SCORE_CONFIG, self.PATH_SCORE_CONFIG)

        # Replacing paths to configurations with paths to package configurations
        else:
            self.PATH_USER_CONFIG = self.__ORIGINAL_PATH_USER_CONFIG
            self.PATH_SCORE_CONFIG = self.__ORIGINAL_PATH_SCORE_CONFIG

    def __load(self) -> None:
        """ Loading all configurations and initializing ConfigManager as dictionary """

        # Set root dictionary from main configuration
        with open(self.PATH_MAIN_CONFIG) as file:
            config: dict = load(file)

        # Mount user configuration to 'user' section of dictionary
        with open(self.PATH_USER_CONFIG) as file:
            config['user'] = load(file)

        # Initializing `list` for scores of attempts
        config['score_list'] = list()

        # Loading score configuration to 'score_list' section of dictionary
        with open(self.PATH_SCORE_CONFIG) as file:
            for line in file.readlines()[1:]:
                score, nick = line.split(',')

                config['score_list'].append((int(score), nick[:-1]))

        # Creating namespace for temporary variables
        config['ns'] = Namespace()

        # Initializing ConfigManager as dictionary
        dict.__init__(self, config)

    def save(self) -> None:
        """ Saves all configurations """

        # Saving user configuration
        with open(self.PATH_USER_CONFIG, 'w') as file:
            dump(self['user'], file, indent=4)

        # Saving scores of attempts
        with open(self.PATH_SCORE_CONFIG, 'w') as file:
            file.write(','.join(('score', 'nick')) + '\n')

            for line in self['score_list']:
                score, nick = line
                file.write(','.join((str(score), nick)) + '\n')

    def reset(self) -> None:
        """ Resets user configurations, replacing them with default configurations """

        if self.USE_USER_CONFIGS:
            # Loading default configurations
            ConfigManager.USE_USER_CONFIGS = False
            self.__init__(self.BASE_DIR)

            # Getting copy of default configurations for the further use
            default_config = self.copy()

            # Loading user configurations
            ConfigManager.USE_USER_CONFIGS = True
            self.__init__(self.BASE_DIR)

            # Replacing user configurations with default configurations
            dict.__init__(self, default_config)

            # Saving new (default) user configurations
            self.save()

    def filter_score(self) -> None:
        """ Fiters scores of attempts. Attempts are sorted by best
            score and then all other attempts are discarded so that
            only the top 5 attempts remain """

        self['score_list'] = list(reversed(sorted(self['score_list'])))[:5]
