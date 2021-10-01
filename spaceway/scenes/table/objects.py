import pygame

from ...mixins import SceneButtonMixin
from ...rect import FloatRect


class TableScore:
    def __init__(self, screen, base_dir, config):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.base_dir = base_dir

        self.config = config

        self.fg_color = (255, 255, 255)
        self.bg_color = (0, 0, 0)
        self.font = pygame.font.Font(f'{base_dir}/assets/fonts/pixeboy.ttf', 36)

        self.border = 1

    def update(self):
        self.msgs = ['Score table']
        self.imgs = []
        self.rects = []

        for line in self.config['score_list']:
            self.msgs.append(str(line[0]) + ' : ' + line[1])

        y = 100 + (6 - len(self.msgs)) * 25

        for line in self.msgs:
            img_fg = self.font.render(line, True, self.fg_color)
            img_bg = self.font.render(line, True, self.bg_color)

            self.imgs.append((img_fg, img_bg))
            rect = img_fg.get_rect()

            rect.centerx = self.screen_rect.centerx
            rect.y = y

            self.rects.append(rect)

            y += 25 if line != 'Score table' else 50

    def blit(self):
        for i in range(len(self.msgs)):
            self.screen.blit(self.imgs[i][1], (self.rects[i].x + self.border, self.rects[i].y))
            self.screen.blit(self.imgs[i][1], (self.rects[i].x - self.border, self.rects[i].y))
            self.screen.blit(self.imgs[i][1], (self.rects[i].x, self.rects[i].y + self.border))
            self.screen.blit(self.imgs[i][1], (self.rects[i].x, self.rects[i].y - self.border))
            self.screen.blit(self.imgs[i][0], self.rects[i])


class TableBackButton(SceneButtonMixin):
    def __init__(self, screen, base_dir, config):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.width = self.height = 63

        self.img = pygame.image.load(f'{base_dir}/assets/images/buttons/back.bmp')
        self.rect = FloatRect(self.img.get_rect())

        self.rect.left = self.screen_rect.left + 5
        self.rect.top = self.screen_rect.bottom - 5

        SceneButtonMixin.__init__(self, base_dir, config, 'table', 'table', 'lobby', 'lobby', 4)

    def keep_move(self):
        if self.action == 'enter':
            return self.rect.bottom > self.screen_rect.bottom - 5
        if self.action == 'leave':
            return self.rect.top < self.screen_rect.bottom
        return False
