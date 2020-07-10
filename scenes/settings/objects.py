import pygame
from json import dump


class EffectsButton(pygame.sprite.Sprite):
    def __init__(self, screen, base_dir, config):
        super().__init__()

        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.width = self.height = 63

        self.config = config

        self.settings_path = f'{base_dir}/config/user.json'

        self.img_true = pygame.image.load(f'{base_dir}/assets/images/buttons/effects_true.bmp')
        self.img_false = pygame.image.load(f'{base_dir}/assets/images/buttons/effects_false.bmp')
        self.img = self.img_false
        self.rect = self.img.get_rect()

        self.rect.center = self.screen_rect.center

        self._screen = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self._screen.fill((0, 0, 0, 0))

        self._rect = pygame.Rect(0, 0, self.width, self.height)
        self._rect.center = self.rect.center

        self.is_save = False

    def save(self):
        with open(self.settings_path, 'w') as file:
            dump(self.config['user'], file, indent=4)

        self.is_save = False


    def update(self):
        self.is_enable = self.config['user']['effects']

        if self.is_enable:
            self.img = self.img_true
        else:
            self.img = self.img_false

        if self.is_save:
            self.save()

        self._rect.center = self.rect.center

    def blit(self):
        self.screen.blit(self._screen, self.rect)
        self.screen.blit(self.img, self.rect)
        self._screen.fill((0, 0, 0, 0), self._rect, pygame.BLEND_RGBA_ADD)


class FullScreenButton(pygame.sprite.Sprite):
    def __init__(self, screen, base_dir, config):
        super().__init__()
        
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.width = self.height = 63

        self.config = config

        self.settings_path = f'{base_dir}/config/user.json'

        self.img_true = pygame.image.load(f'{base_dir}/assets/images/buttons/full_screen_true.bmp')
        self.img_false = pygame.image.load(f'{base_dir}/assets/images/buttons/full_screen_false.bmp')
        self.img = self.img_false
        self.rect = self.img.get_rect()

        self.rect.center = self.screen_rect.center

        self._screen = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self._screen.fill((0, 0, 0, 0))

        self._rect = pygame.Rect(0, 0, self.width, self.height)
        self._rect.center = self.rect.center

        self.is_save = False

    def save(self):
        with open(self.settings_path, 'w') as file:
            dump(self.config['user'], file, indent=4)

        self.is_save = False


    def update(self):
        self.is_enable = self.config['user']['full_screen']

        if self.is_enable:
            self.img = self.img_true
        else:
            self.img = self.img_false

        if self.is_save:
            self.save()

        self._rect.center = self.rect.center

    def blit(self):
        self.screen.blit(self._screen, self.rect)
        self.screen.blit(self.img, self.rect)
        self._screen.fill((0, 0, 0, 0), self._rect, pygame.BLEND_RGBA_ADD)


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

        if self.is_save:
            self.save()

        self._rect.center = self.rect.center

    def blit(self):
        self.screen.blit(self._screen, self.rect)
        self.screen.blit(self.img, self.rect)
        self.screen.blit(self._img, self._img_rect)
        self._screen.fill((0, 0, 0, 0), self._rect, pygame.BLEND_RGBA_ADD)
