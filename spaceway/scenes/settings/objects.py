import pygame

from ...mixins import SettingsButtonMixin, SceneButtonMixin
from ...rect import FloatRect


class EffectsButton(SettingsButtonMixin):
    def __init__(self, screen, base_dir, config):
        self.width = self.height = 63

        self.imgs = {True: pygame.image.load(f'{base_dir}/assets/images/buttons/effects_true.bmp'),
                     False: pygame.image.load(f'{base_dir}/assets/images/buttons/effects_false.bmp')}

        SettingsButtonMixin.__init__(self, screen, config, 'effects')


class FullScreenButton(SettingsButtonMixin):
    def __init__(self, screen, base_dir, config):
        self.width = self.height = 63

        self.imgs = {True: pygame.image.load(f'{base_dir}/assets/images/buttons/full_screen_true.bmp'),
                     False: pygame.image.load(f'{base_dir}/assets/images/buttons/full_screen_false.bmp')}

        self.changed = False

        SettingsButtonMixin.__init__(self, screen, config, 'full_screen')

    def change_state(self):
        SettingsButtonMixin.change_state(self)
        self.changed = True


class UpdatesButton(SettingsButtonMixin):
    def __init__(self, screen, base_dir, config):
        self.width = self.height = 63

        self.imgs = {True: pygame.image.load(f'{base_dir}/assets/images/buttons/updates_true.bmp'),
                     False: pygame.image.load(f'{base_dir}/assets/images/buttons/updates_false.bmp')}

        SettingsButtonMixin.__init__(self, screen, config, 'updates')


class DifficultyButton(SettingsButtonMixin):
    def __init__(self, screen, base_dir, config):
        self.width = self.height = 63

        self.imgs = {0: pygame.image.load(f'{base_dir}/assets/images/buttons/difficulty_easy.bmp'),
                     1: pygame.image.load(f'{base_dir}/assets/images/buttons/difficulty_middle.bmp'),
                     2: pygame.image.load(f'{base_dir}/assets/images/buttons/difficulty_hard.bmp'),
                     3: pygame.image.load(f'{base_dir}/assets/images/buttons/difficulty_insanse.bmp')}

        SettingsButtonMixin.__init__(self, screen, config, 'difficulty')

    def change_state(self):
        self.state = (self.state + 1) % 4


class SettingsBackButton(SceneButtonMixin):
    def __init__(self, screen, base_dir, config):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.width = self.height = 63

        self.img = pygame.image.load(f'{base_dir}/assets/images/buttons/back.bmp')
        self.rect = FloatRect(self.img.get_rect())

        self.rect.left = self.screen_rect.left + 5
        self.rect.top = self.screen_rect.bottom - 5

        SceneButtonMixin.__init__(self, base_dir, config, 'settings', 'settings', 'lobby', 'lobby', 4)

    def keep_move(self):
        if self.action == 'enter':
            return self.rect.bottom > self.screen_rect.bottom - 5
        if self.action == 'leave':
            return self.rect.top < self.screen_rect.bottom
        return False


class NickInput:
    def __init__(self, screen, base_dir, config):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.width = 315
        self.height = 42
        self.fg_color = (0, 0, 0)
        self.bg_color = (255, 255, 255)
        self.font = pygame.font.Font(f'{base_dir}/assets/fonts/pixeboy.ttf', 36)

        self.config = config

        self.settings_path = f'{base_dir}/config/user.json'

        self.img_disable = pygame.image.load(f'{base_dir}/assets/images/inputs/nick_disable.bmp')
        self.img_enable = pygame.image.load(f'{base_dir}/assets/images/inputs/nick_enable.bmp')
        self.img = self.img_disable
        self.rect = self.img.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery - 74

        self.is_enable = False

    def update(self):
        if self.is_enable:
            self.img = self.img_enable
        else:
            self.img = self.img_disable

        self._img = self.font.render(self.config['user']['nick'][-17:], True, self.fg_color, self.bg_color)
        self._rect = self._img.get_rect()
        self._rect.center = self.rect.center

    def blit(self):
        self.screen.blit(self.img, self.rect)
        self.screen.blit(self._img, self._rect)
