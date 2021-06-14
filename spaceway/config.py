from json import load, dump


class ConfigManager(dict):
    def __init__(self, base_dir):
        self.CONFIG_PATH = f'{base_dir}/config/config.json'
        self.USER_CONFIG_PATH = f'{base_dir}/config/user.json'
        self.SCORE_PATH = f'{base_dir}/config/score.csv'

        self.load()

    def load(self) -> None:
        config = {}

        with open(self.CONFIG_PATH) as file:
            config = load(file)

        with open(self.USER_CONFIG_PATH) as file:
            config['user'] = load(file)

        config['score_list'] = self.__load_score()

        dict.__init__(self, config)

    def save(self) -> None:
        config = dict(self)

        with open(self.USER_CONFIG_PATH, 'w') as file:
            dump(config['user'], file, indent=4)

        self.__save_score(config['score_list'])

    def filter_score(self) -> None:
        self['score_list'] = list(reversed(sorted(self['score_list'])))[:5]

    def __save_score(self, score_list: list) -> None:
        with open(self.SCORE_PATH, 'w') as file:
            file.write(','.join(('score', 'nick')) + '\n')

            for line in score_list:
                score, nick = line
                file.write(','.join((str(score), nick)) + '\n')

    def __load_score(self) -> list:
        score_list = []

        with open(self.SCORE_PATH) as file:
            for line in file.readlines()[1:]:
                score, nick = line.split(',')

                score_list.append((int(score), nick[:-1]))

        return score_list
