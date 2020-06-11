import pygame


class PlayButton:
    def __init__(self, screen, base_dir, config):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.width = self.height = 90

        self.config = config

        self.img_idle = pygame.image.load(f'{base_dir}/assets/images/buttons/play.bmp')
        self.img = self.img_idle
        self.rect = self.img.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.top

        self._screen = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self._screen.fill((0, 0, 0, 0))

        self._rect = pygame.Rect(0, 0, self.width, self.height)
        self._rect.centerx = self.rect.centerx
        self._rect.centery = self.rect.centery

        self.to_bottom = True
        self.to_top = False
        self.change_scene = False

    def update(self):

        if self.to_bottom:
            if self.rect.centery + 15 <= self.screen_rect.centery:
                self.rect.y += 15
            else:
                self.to_bottom = False

        if self.to_top:
            if self.rect.bottom >= self.screen_rect.top:
                self.rect.y -= 15
            else:
                self.to_top = False

                if self.change_scene:
                    self.change_scene = False
                    self.config['scene'] = 'game'

        self._rect.center = self.rect.center

    def blit(self):
        self.screen.blit(self._screen, self.rect)
        self.screen.blit(self.img, self.rect)
        self._screen.fill((0, 0, 0, 0), self._rect, pygame.BLEND_RGBA_ADD)


class TableButton:
    def __init__(self, screen, base_dir, config):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.width = self.height = 63

        self.config = config

        self.img_idle = pygame.image.load(f'{base_dir}/assets/images/buttons/table.bmp')
        self.img = self.img_idle
        self.rect = self.img.get_rect()

        self.rect.left = self.screen_rect.left + 5
        self.rect.top = self.screen_rect.bottom - 5

        self._screen = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self._screen.fill((0, 0, 0, 0))

        self._rect = pygame.Rect(0, 0, self.width, self.height)
        self._rect.centerx = self.rect.centerx
        self._rect.centery = self.rect.centery

        self.to_bottom = False
        self.to_top = True
        self.change_scene = False

    def update(self):

        if self.to_bottom:
            if self.rect.top <= self.screen_rect.bottom:
                self.rect.y += 4
            else:
                self.to_bottom = False

                if self.change_scene:
                    self.change_scene = False
                    self.config['scene'] = 'table'

        if self.to_top:
            if self.rect.bottom + 5 >= self.screen_rect.bottom:
                self.rect.y -= 4
            else:
                self.to_top = False

        self._rect.center = self.rect.center

    def blit(self):
        self.screen.blit(self._screen, self.rect)
        self.screen.blit(self.img, self.rect)
        self._screen.fill((0, 0, 0, 0), self._rect, pygame.BLEND_RGBA_ADD)
