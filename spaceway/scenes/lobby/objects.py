import pygame

from ...mixins import FloatButtonMixin, CaptionMixin


class PlayButton(FloatButtonMixin):
    def __init__(self, screen, base_dir, config):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.width = self.height = 90

        self.scene = 'game'
        self.speed = 16

        self.img = pygame.image.load(f'{base_dir}/assets/images/buttons/play.bmp')
        self.rect = self.img.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.top

        FloatButtonMixin.__init__(self, base_dir, config, 'top')


class TableButton(FloatButtonMixin):
    def __init__(self, screen, base_dir, config):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.width = self.height = 63

        self.scene = 'table'
        self.speed = 4

        self.img = pygame.image.load(f'{base_dir}/assets/images/buttons/table.bmp')
        self.rect = self.img.get_rect()

        self.rect.left = self.screen_rect.left + 5
        self.rect.top = self.screen_rect.bottom - 5

        FloatButtonMixin.__init__(self, base_dir, config, 'bottom')


class SettingsButton(FloatButtonMixin):
    def __init__(self, screen, base_dir, config):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.width = self.height = 63

        self.scene = 'settings'
        self.speed = 4

        self.img = pygame.image.load(f'{base_dir}/assets/images/buttons/settings.bmp')
        self.rect = self.img.get_rect()

        self.rect.right = self.screen_rect.right - 5
        self.rect.top = self.screen_rect.bottom - 5

        FloatButtonMixin.__init__(self, base_dir, config, 'bottom')


class Caption(CaptionMixin):
    def __init__(self, screen, base_dir, config, caption='Space Way'):
        CaptionMixin.__init__(self, base_dir, config, caption)

        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.y = 100

    def blit(self):
        self._blit()
