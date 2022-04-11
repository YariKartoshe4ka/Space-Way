import pygame

from ...mixins import CaptionMixin, SceneButtonMixin
from ...hitbox import Ellipse


class PlayButton(SceneButtonMixin):
    def __init__(self, screen, base_dir, config):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.img = pygame.image.load(f'{base_dir}/assets/images/buttons/play.bmp')
        self.rect = Ellipse(self.img.get_rect())

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.top

        SceneButtonMixin.__init__(self, base_dir, config, 'lobby', 'lobby', 'game', 'game',
                                  -16, self.rect.top, self.screen_rect.centery - self.rect.h / 2, 'enter')


class TableButton(SceneButtonMixin):
    def __init__(self, screen, base_dir, config):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.img = pygame.image.load(f'{base_dir}/assets/images/buttons/table.bmp')
        self.rect = Ellipse(self.img.get_rect())

        self.rect.left = self.screen_rect.left + 5
        self.rect.top = self.screen_rect.bottom

        SceneButtonMixin.__init__(self, base_dir, config, 'lobby', 'lobby', 'table', 'table',
                                  4, self.screen_rect.bottom - self.rect.h - 5, self.rect.top, 'enter')

    def press(self):
        self.config['ns'].table.update()
        SceneButtonMixin.press(self)


class SettingsButton(SceneButtonMixin):
    def __init__(self, screen, base_dir, config):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.img = pygame.image.load(f'{base_dir}/assets/images/buttons/settings.bmp')
        self.rect = Ellipse(self.img.get_rect())

        self.rect.right = self.screen_rect.right - 5
        self.rect.top = self.screen_rect.bottom

        SceneButtonMixin.__init__(self, base_dir, config, 'lobby', 'lobby', 'settings', 'settings',
                                  4, self.screen_rect.bottom - self.rect.h - 5, self.rect.top, 'enter')


class Caption(CaptionMixin, pygame.sprite.Sprite):
    def __init__(self, screen, base_dir, config):
        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        CaptionMixin.__init__(self, base_dir, config, 'Space Way')

    def locate(self):
        self.rect.centerx = self.screen_rect.centerx
        self.rect.y = 100
