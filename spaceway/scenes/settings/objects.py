import re

import pygame

from ...mixins import SettingsButtonMixin, SceneButtonMixin
from ...music import SoundGroup
from ...hitbox import Ellipse


class EffectsButton(SettingsButtonMixin):
    def __init__(self, screen, base_dir, config):
        self.imgs = {0: pygame.image.load(f'{base_dir}/assets/images/buttons/effects_0.bmp'),
                     0.25: pygame.image.load(f'{base_dir}/assets/images/buttons/effects_25.bmp'),
                     0.5: pygame.image.load(f'{base_dir}/assets/images/buttons/effects_50.bmp'),
                     0.75: pygame.image.load(f'{base_dir}/assets/images/buttons/effects_75.bmp'),
                     1: pygame.image.load(f'{base_dir}/assets/images/buttons/effects_100.bmp')}

        self.hints = {0: 'Enable sound effects like bumps',
                      0.25: 'Increase volume of effects',
                      0.5: 'Increase volume of effects',
                      0.75: 'Increase volume of effects',
                      1: 'Disable sound effects like bumps'}

        SettingsButtonMixin.__init__(self, screen, base_dir, config, 'effects')

    def change_state(self):
        states = list(self.imgs)
        self.state = states[(states.index(self.state) + 1) % len(states)]
        self.config['ns'].mm.set_volume(self.state, SoundGroup.EFFECT)


class MusicButton(SettingsButtonMixin):
    def __init__(self, screen, base_dir, config):
        self.imgs = {0: pygame.image.load(f'{base_dir}/assets/images/buttons/music_0.bmp'),
                     0.25: pygame.image.load(f'{base_dir}/assets/images/buttons/music_25.bmp'),
                     0.5: pygame.image.load(f'{base_dir}/assets/images/buttons/music_50.bmp'),
                     0.75: pygame.image.load(f'{base_dir}/assets/images/buttons/music_75.bmp'),
                     1: pygame.image.load(f'{base_dir}/assets/images/buttons/music_100.bmp')}

        self.hints = {0: 'Enable background music',
                      0.25: 'Increase volume of music',
                      0.5: 'Increase volume of music',
                      0.75: 'Increase volume of music',
                      1: 'Disable background music'}

        SettingsButtonMixin.__init__(self, screen, base_dir, config, 'music')

    def change_state(self):
        states = list(self.imgs)
        self.state = states[(states.index(self.state) + 1) % len(states)]
        self.config['ns'].mm.set_volume(self.state, SoundGroup.SOUND)


class FullScreenButton(SettingsButtonMixin):
    def __init__(self, screen, base_dir, config):
        self.imgs = {True: pygame.image.load(f'{base_dir}/assets/images/buttons/full_screen_true.bmp'),
                     False: pygame.image.load(f'{base_dir}/assets/images/buttons/full_screen_false.bmp')}

        self.hints = {True: 'Quit from fullscreen mode',
                      False: 'Enter to fullscreen mode'}

        self.changed = False

        SettingsButtonMixin.__init__(self, screen, base_dir, config, 'full_screen')

    def change_state(self):
        SettingsButtonMixin.change_state(self)
        self.changed = True


class UpdatesButton(SettingsButtonMixin):
    def __init__(self, screen, base_dir, config):
        self.imgs = {True: pygame.image.load(f'{base_dir}/assets/images/buttons/updates_true.bmp'),
                     False: pygame.image.load(f'{base_dir}/assets/images/buttons/updates_false.bmp')}

        self.hints = {True: 'Disable update notifications',
                      False: 'Enable update notifications'}

        SettingsButtonMixin.__init__(self, screen, base_dir, config, 'updates')


class SettingsBackButton(SceneButtonMixin):
    def __init__(self, screen, base_dir, config):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.img = pygame.image.load(f'{base_dir}/assets/images/buttons/back.bmp')
        self.rect = Ellipse(self.img.get_rect())

        self.rect.left = self.screen_rect.left + 5
        self.rect.top = self.screen_rect.bottom

        SceneButtonMixin.__init__(self, base_dir, config, 'settings', 'settings', 'lobby', 'lobby',
                                  4, self.screen_rect.bottom - self.rect.h - 5, self.rect.top, 4)


class NickInput:
    TICK_INTERVAL = 0.7

    def __init__(self, screen, base_dir, config):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.fg_color = (0, 0, 0)
        self.font = pygame.font.Font(f'{base_dir}/assets/fonts/pixeboy.ttf', 36)

        self.config = config

        self.settings_path = f'{base_dir}/config/user.json'

        self.imgs = {
            0: pygame.image.load(f'{base_dir}/assets/images/inputs/nick_disable.bmp'),
            1: pygame.image.load(f'{base_dir}/assets/images/inputs/nick_enable.bmp'),
            2: pygame.image.load(f'{base_dir}/assets/images/inputs/nick_wrong.bmp')
        }

        self.state = 0
        self.img = self.imgs[self.state]
        self.rect = self.img.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery - 74

        self.tick = self.TICK_INTERVAL

    def update(self):
        self.img = self.imgs[self.state]

        self.img_font = self.font.render(self.config['user']['nick'], True, self.fg_color)
        self.rect_font = self.img_font.get_rect()

        self.rect_font.center = self.rect.center

        self.img_cursor = pygame.Surface((13, 25))
        self.rect_cursor = self.img_cursor.get_rect()

        self.rect_cursor.left = self.rect_font.right + 2
        self.rect_cursor.centery = self.rect_font.centery - 1

        if self.state > 0:
            self.tick %= self.TICK_INTERVAL * 2
            self.tick += self.config['ns'].dt / 30

    def blit(self):
        self.screen.blit(self.img, self.rect)
        self.screen.blit(self.img_font, self.rect_font)

        if self.state > 0 and self.tick > 0.7:
            self.screen.blit(self.img_cursor, self.rect_cursor)

    def enable(self):
        self.tick = self.TICK_INTERVAL
        self.state = 1
        pygame.key.start_text_input()

    def disable(self):
        self.state = 0
        pygame.key.stop_text_input()

    def add_char(self, char):
        if self.state == 0 or not char:
            return

        self.state = 1

        if char == '\r':
            self.state = 0

        elif char == '\b':
            self.config['user']['nick'] = self.config['user']['nick'][:-1]

        elif re.match(r'^[\w!?:; \(\)]{1,15}$', self.config['user']['nick'] + char, flags=re.ASCII):
            self.config['user']['nick'] += char

        else:
            self.state = 2
