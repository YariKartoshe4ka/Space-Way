import pygame

from ...mixins import CaptionMixin
from ...rect import FloatRect


class Text(CaptionMixin):
    def __init__(self, screen, base_dir, config):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.img_bg = pygame.image.load(f'{base_dir}/assets/images/background/headpiece.bmp')
        self.rect_bg = self.img_bg.get_rect()

        self.img_heart = pygame.image.load(f'{base_dir}/assets/images/heart/heart.bmp')
        self.rect_heart = self.img_heart.get_rect()
        self.is_heart = False

        self.base_dir = base_dir

        CaptionMixin.__init__(self, base_dir, config, 'YariKartoshe4ka')

    def update(self):
        if self.config['ns'].tick % (self.config['FPS'] * 4) == 0:
            self.config['scene'] = self.config['sub_scene'] = 'lobby'

        elif self.config['ns'].tick % (self.config['FPS'] * 2) == 0:
            self.caption = 'With love'
            self.is_heart = True

        CaptionMixin.update(self)

    def blit(self):
        self.screen.blit(self.img_bg, self.rect_bg)

        if self.is_heart:
            self.screen.blit(self.img_heart, self.rect_heart)

        CaptionMixin.blit(self)

    def locate(self):
        self.rect.y = 50
        self.rect.centerx = self.screen_rect.centerx

        if self.is_heart:
            self.rect_heart.centery = self.rect.centery

            self.rect.centerx -= self.rect_heart.width - 5
            self.rect_heart.left = self.rect.right + 5


class ProgressBar:
    def __init__(self, screen, base_dir, config):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.config = config
        self.color = (
            (0, 153, 255),
            (252, 15, 192),
            (0, 255, 0)
        )[self.config['user']['color']]

        self.line = FloatRect(0, self.config['mode'][1] - 5, 0, 5)
        self.inc = self.config['mode'][0] / (self.config['FPS'] * 4)

        self.font = pygame.font.Font(f'{base_dir}/assets/fonts/pixeboy.ttf', 22)

    def update(self):
        self.line.width += self.inc

        self.img = self.font.render(f"{round(self.line.width * 100 / self.config['mode'][0])}%", True, self.color)
        self.rect = self.img.get_rect()

        self.rect.centerx = max(
            self.line.left + self.rect.width // 2 + 5,
            min(self.line.right, self.config['mode'][0] - self.rect.width // 2 - 5)
        )
        self.rect.bottom = self.line.top - 5

    def blit(self):
        pygame.draw.rect(self.screen, self.color, self.line)
        self.screen.blit(self.img, self.rect)
