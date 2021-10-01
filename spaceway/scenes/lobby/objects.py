import pygame

from ...mixins import CaptionMixin, SceneButtonMixin
from ...rect import FloatRect


class PlayButton(SceneButtonMixin):
    def __init__(self, screen, base_dir, config):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.width = self.height = 90

        self.img = pygame.image.load(f'{base_dir}/assets/images/buttons/play.bmp')
        self.rect = FloatRect(self.img.get_rect())

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.top

        SceneButtonMixin.__init__(self, base_dir, config, 'lobby', 'lobby',
                                  'game', 'game', -16, 'enter')

    def keep_move(self):
        if self.action == 'enter':
            return self.rect.centery < self.screen_rect.centery
        if self.action == 'leave':
            return self.rect.bottom > self.screen_rect.top
        return False


class TableButton(SceneButtonMixin):
    def __init__(self, screen, base_dir, config):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.width = self.height = 63

        self.img = pygame.image.load(f'{base_dir}/assets/images/buttons/table.bmp')
        self.rect = FloatRect(self.img.get_rect())

        self.rect.left = self.screen_rect.left + 5
        self.rect.top = self.screen_rect.bottom

        SceneButtonMixin.__init__(self, base_dir, config, 'lobby', 'lobby',
                                  'table', 'table', 4, 'enter')

    def keep_move(self):
        if self.action == 'enter':
            return self.rect.bottom > self.screen_rect.bottom - 5
        if self.action == 'leave':
            return self.rect.top < self.screen_rect.bottom
        return False


class SettingsButton(SceneButtonMixin):
    def __init__(self, screen, base_dir, config):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.width = self.height = 63

        self.img = pygame.image.load(f'{base_dir}/assets/images/buttons/settings.bmp')
        self.rect = FloatRect(self.img.get_rect())

        self.rect.right = self.screen_rect.right - 5
        self.rect.top = self.screen_rect.bottom

        SceneButtonMixin.__init__(self, base_dir, config, 'lobby', 'lobby',
                                  'settings', 'settings', 4, 'enter')

    def keep_move(self):
        if self.action == 'enter':
            return self.rect.bottom > self.screen_rect.bottom - 5
        if self.action == 'leave':
            return self.rect.top < self.screen_rect.bottom
        return False


class Caption(CaptionMixin, pygame.sprite.Sprite):
    def __init__(self, screen, base_dir, config):
        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        CaptionMixin.__init__(self, base_dir, config, 'Space Way')

    def locate(self):
        self.rect.centerx = self.screen_rect.centerx
        self.rect.y = 100
