from json import dump

import pygame

from ...mixins import ButtonMixin


class EffectsButton(ButtonMixin, pygame.sprite.Sprite):
    def __init__(self, screen, base_dir, config):
        pygame.sprite.Sprite.__init__(self)

        self.width = self.height = 63

        self.index = 'effects'

        self.imgs = {'true':  pygame.image.load(f'{base_dir}/assets/images/buttons/effects_true.bmp'),
                     'false': pygame.image.load(f'{base_dir}/assets/images/buttons/effects_false.bmp')}

        ButtonMixin.__init__(self, screen, base_dir, config, True)


class FullScreenButton(ButtonMixin, pygame.sprite.Sprite):
    def __init__(self, screen, base_dir, config):
        pygame.sprite.Sprite.__init__(self)

        self.width = self.height = 63

        self.index = 'full_screen'

        self.imgs = {'true':  pygame.image.load(f'{base_dir}/assets/images/buttons/full_screen_true.bmp'),
                     'false': pygame.image.load(f'{base_dir}/assets/images/buttons/full_screen_false.bmp')}

        ButtonMixin.__init__(self, screen, base_dir, config, True)

        self.changed = self.config['user'][self.index]


class DifficultyButton(ButtonMixin, pygame.sprite.Sprite):
    def __init__(self, screen, base_dir, config):
        pygame.sprite.Sprite.__init__(self)

        self.width = self.height = 63

        self.index = 'difficulty'

        self.imgs = {'easy': pygame.image.load(f'{base_dir}/assets/images/buttons/difficulty_easy.bmp'),
                     'middle': pygame.image.load(f'{base_dir}/assets/images/buttons/difficulty_middle.bmp'),
                     'hard': pygame.image.load(f'{base_dir}/assets/images/buttons/difficulty_hard.bmp'),
                     'insanse': pygame.image.load(f'{base_dir}/assets/images/buttons/difficulty_insanse.bmp')}

        ButtonMixin.__init__(self, screen, base_dir, config, True)

    def change_image(self):
        if self.state == 0:
            self.img = self.imgs['easy']
        elif self.state == 1:
            self.img = self.imgs['middle']
        elif self.state == 2:
            self.img = self.imgs['hard']
        elif self.state == 3:
            self.img = self.imgs['insanse']


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

        self._screen = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self._screen.fill((0, 0, 0, 0))

        self._rect = pygame.Rect(0, 0, self.width, self.height)
        self._rect.center = self.rect.center

        self.is_save = False
        self.is_enable = False

    def save(self):
        if self.is_save:
            with open(self.settings_path, 'w') as file:
                dump(self.config['user'], file, indent=4)

            self.is_save = False

    def update(self):
        if self.is_enable:
            self.img = self.img_enable
        else:
            self.img = self.img_disable

        self._img = self.font.render(self.config['user']['nick'][-17:], True, self.fg_color, self.bg_color)
        self._img_rect = self._img.get_rect()
        self._img_rect.center = self.rect.center

        self._rect.center = self.rect.center

    def blit(self):
        self.screen.blit(self._screen, self.rect)
        self.screen.blit(self.img, self.rect)
        self.screen.blit(self._img, self._img_rect)
        self._screen.fill((0, 0, 0, 0), self._rect, pygame.BLEND_RGBA_ADD)
