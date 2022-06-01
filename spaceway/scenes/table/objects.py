import pygame

from ...boost import render
from ...mixins import SceneButtonMixin
from ...hitbox import Ellipse


class TableScore:
    def __init__(self, screen, base_dir, config):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.base_dir = base_dir

        self.config = config

        self.colors = {
            'fg': (255, 255, 255),
            'bg': (14, 5, 22),
            'gold': (253, 170, 0),
            'silver': (176, 176, 176),
            'bronze': (189, 111, 34)
        }

        self.font_caption = pygame.font.Font(f'{base_dir}/assets/fonts/pixeboy.ttf', 40)
        self.font = pygame.font.Font(f'{base_dir}/assets/fonts/pixeboy.ttf', 32)

        self.img_caption = render(self.font_caption, 'Score table', self.colors['fg'], 2, self.colors['bg'])

    def update(self):
        self.img_nicks = []
        self.rect_nicks = []

        self.img_scores = []
        self.rect_scores = []

        last_nick_rect = last_score_rect = pygame.Rect(0, 0, 0, 0)

        for i, info in enumerate(self.config['score_list']):
            score, nick = info

            self.img_nicks.append(render(self.font, nick, self.colors['fg'], 2, self.colors['bg']))
            last_nick_rect = self.img_nicks[-1].get_rect().move(0, last_nick_rect.bottom)
            self.rect_nicks.append(last_nick_rect)

            color_score = self.colors['fg']

            if i == 0:
                color_score = self.colors['gold']
            elif i == 1:
                color_score = self.colors['silver']
            elif i == 2:
                color_score = self.colors['bronze']

            self.img_scores.append(render(self.font, str(score), color_score, 2, self.colors['bg']))
            last_score_rect = self.img_scores[-1].get_rect().move(0, last_score_rect.bottom)
            self.rect_scores.append(last_score_rect)

        # Union rects and prepare for centering
        rect_all_nicks = last_nick_rect.unionall(self.rect_nicks)

        rect_all_scores = last_score_rect.unionall(self.rect_scores)
        rect_all_scores.left = rect_all_nicks.right + 35

        self.rect_caption = self.img_caption.get_rect()
        self.rect_caption.bottom = rect_all_nicks.top - 25

        rect_all = self.rect_caption.unionall([rect_all_nicks, rect_all_scores])
        rect_all.center = self.screen_rect.center
        rect_all.y -= 35

        # Center all rects
        self.rect_caption.top = rect_all.top
        self.rect_caption.centerx = rect_all.centerx

        rect_all_nicks.bottomleft = rect_all.bottomleft
        rect_all_scores.bottomright = rect_all.bottomright

        for rect_nick in self.rect_nicks:
            rect_nick.centerx = rect_all_nicks.centerx
            rect_nick.y += rect_all_nicks.y

        for rect_score in self.rect_scores:
            rect_score.centerx = rect_all_scores.centerx
            rect_score.y += rect_all_scores.y

    def blit(self):
        self.screen.blit(self.img_caption, self.rect_caption)

        for i in range(len(self.img_nicks)):
            self.screen.blit(self.img_nicks[i], self.rect_nicks[i])
            self.screen.blit(self.img_scores[i], self.rect_scores[i])


class TableBackButton(SceneButtonMixin):
    def __init__(self, screen, base_dir, config):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.img = pygame.image.load(f'{base_dir}/assets/images/buttons/back.bmp')
        self.rect = Ellipse(self.img.get_rect())

        self.rect.left = self.screen_rect.left + 5
        self.rect.top = self.screen_rect.bottom

        SceneButtonMixin.__init__(self, base_dir, config, 'table', 'table', 'lobby', 'lobby',
                                  4, self.screen_rect.bottom - self.rect.h - 5, self.rect.top, 4)
