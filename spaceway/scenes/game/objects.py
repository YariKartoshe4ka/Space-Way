from random import randint

import pygame

from ...mixins import BoostMixin, CaptionMixin, SceneButtonMixin
from ...rect import FloatRect


class Background:
    def __init__(self, screen, base_dir, config):
        self.screen = screen

        self.config = config

        self.img = pygame.image.load(f'{base_dir}/assets/images/bg/background.bmp')
        self.rect = FloatRect(self.img.get_rect())

    def update(self):
        self.rect.x -= 0.5 * self.config['ns'].dt

        if self.rect.x <= -840:
            self.rect.x = 0

    def blit(self):
        self.screen.blit(self.img, self.rect)


class SpacePlate(pygame.sprite.Sprite):
    def __init__(self, screen, base_dir, config):
        super().__init__()

        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.config = config

        self.flip = False

        self.imgs = [pygame.image.load(f'{base_dir}/assets/images/plate/blue.bmp'),
                     pygame.image.load(f'{base_dir}/assets/images/plate/pink.bmp'),
                     pygame.image.load(f'{base_dir}/assets/images/plate/green.bmp')]

        self.is_flame = False
        self.img_flame = pygame.image.load(f'{base_dir}/assets/images/plate/flame.bmp')
        self.img_flame_flip = pygame.transform.flip(self.img_flame, False, True)
        self.rect_flame = self.img_flame.get_rect()

        self.img = self.imgs[self.config['user']['color']]
        self.img_flip = pygame.transform.flip(self.img, False, True)
        self.rect = FloatRect(self.img.get_rect())

        self.rect.x = 5
        self.rect.centery = self.screen_rect.centery

        self.rect_flame.centerx = self.rect.centerx + 1

        self.gravity_default = 7
        self.gravity = self.gravity_default
        self.gravity_scale = 0.25

        self.is_jump = False
        self.jump = 10
        self.sounds = {'jump': f'{base_dir}/assets/sounds/jump.wav',
                       'bang': f'{base_dir}/assets/sounds/bang.wav',
                       'score': f'{base_dir}/assets/sounds/score.wav'}

    def reset(self):
        self.rect.centery = self.screen_rect.centery
        self.is_jump = False
        self.jump = 10
        self.is_flame = False
        self.gravity = self.gravity_default
        self.flip = False

    def update(self):
        if self.img != self.imgs[self.config['user']['color']]:
            self.img = self.imgs[self.config['user']['color']]
            self.img_flip = pygame.transform.flip(self.img, False, True)

        if not self.is_jump:
            self.gravity += self.gravity_scale * self.config['ns'].dt
            if self.flip:
                self.rect.y -= self.gravity * self.config['ns'].dt
            else:
                self.rect.y += self.gravity * self.config['ns'].dt
        else:
            self.gravity = self.gravity_default

            if self.jump >= -5:
                inc = self.jump ** 2 // 3 * self.config['ns'].dt
                if self.jump < 0:
                    self.is_flame = False
                    self.rect.y += -inc if self.flip else inc
                else:
                    self.is_flame = True
                    self.rect.y += inc if self.flip else -inc
                self.jump -= 1 * self.config['ns'].dt
            else:
                self.is_jump = False
                self.jump = 10

        if self.flip:
            self.rect_flame.bottom = self.rect.top
        else:
            self.rect_flame.top = self.rect.bottom

    def blit(self):
        if self.flip:
            self.screen.blit(self.img_flip, self.rect)
            if self.is_flame:
                self.screen.blit(self.img_flame_flip, self.rect_flame)
        else:
            self.screen.blit(self.img, self.rect)
            if self.is_flame:
                self.screen.blit(self.img_flame, self.rect_flame)


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, screen, base_dir, config):
        super().__init__()

        self.name = 'simple'

        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.config = config

        self.img_idle = pygame.image.load(f'{base_dir}/assets/images/asteroid/gray_idle.bmp')
        self.img = self.img_idle

        self.rect = FloatRect(self.img.get_rect())
        self.rect.y = randint(1, self.screen_rect.height - self.rect.height - 2)

        self.rect.left = self.screen_rect.right

    def blit(self):
        self.screen.blit(self.img, self.rect)

    def update(self):
        self.rect.x -= self.config['ns'].speed * self.config['ns'].dt


class FlyingAsteroid(pygame.sprite.Sprite):
    def __init__(self, screen, base_dir, config):
        super().__init__()

        self.name = 'flying'

        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.config = config

        self.imgs = [pygame.image.load(f'{base_dir}/assets/images/asteroid/red_idle.bmp'),
                     pygame.image.load(f'{base_dir}/assets/images/asteroid/blue_idle.bmp')]

        self.img = self.imgs[randint(0, 1)]

        self.rect = FloatRect(self.img.get_rect())
        self.rect.bottom = self.screen_rect.top
        self.rect.left = self.screen_rect.right

    def blit(self):
        self.screen.blit(self.img, self.rect)

    def update(self):
        self.rect.x -= self.config['ns'].speed * 1.5 * self.config['ns'].dt
        self.rect.y += self.config['ns'].speed * self.config['ns'].dt


class TimeBoost(BoostMixin, pygame.sprite.Sprite):
    def __init__(self, screen, base_dir, config, life=5):
        pygame.sprite.Sprite.__init__(self)

        self.speed = 2

        self.img_idle = pygame.image.load(f'{base_dir}/assets/images/boosts/time_idle.bmp')
        self.img_small = pygame.image.load(f'{base_dir}/assets/images/boosts/time_small.bmp')

        BoostMixin.__init__(self, screen, base_dir, config, 'time', life)

    def activate(self):
        self.is_active = True
        self.speed = self.config['ns'].speed
        self.config['ns'].speed = 2

    def deactivate(self):
        self.config['ns'].speed = self.speed


class DoubleBoost(BoostMixin, pygame.sprite.Sprite):
    def __init__(self, screen, base_dir, config, life=5):
        pygame.sprite.Sprite.__init__(self)

        self.img_idle = pygame.image.load(f'{base_dir}/assets/images/boosts/double_idle.bmp')
        self.img_small = pygame.image.load(f'{base_dir}/assets/images/boosts/double_small.bmp')

        BoostMixin.__init__(self, screen, base_dir, config, 'double', life)


class ShieldBoost(BoostMixin, pygame.sprite.Sprite):
    def __init__(self, screen, base_dir, config, plate, life=5):
        pygame.sprite.Sprite.__init__(self)

        self.plate = plate

        self.img_idle = pygame.image.load(f'{base_dir}/assets/images/boosts/shield_idle.bmp')
        self.img_small = pygame.image.load(f'{base_dir}/assets/images/boosts/shield_small.bmp')
        self.img_active = pygame.image.load(f'{base_dir}/assets/images/boosts/shield_activate.bmp')

        self.rect_active = FloatRect(self.img_active.get_rect())

        BoostMixin.__init__(self, screen, base_dir, config, 'shield', life)

    def update(self):
        BoostMixin.update(self)

        if self.is_active:
            self.rect_active.center = self.plate.rect.center

    def blit(self):
        BoostMixin.blit(self)

        if self.is_active:
            self.screen.blit(self.img_active, self.rect_active)


class MirrorBoost(BoostMixin, pygame.sprite.Sprite):
    def __init__(self, screen, base_dir, config, plate, life=5):
        pygame.sprite.Sprite.__init__(self)

        self.plate = plate

        self.img_idle = pygame.image.load(f'{base_dir}/assets/images/boosts/mirror_idle.bmp')
        self.img_small = pygame.image.load(f'{base_dir}/assets/images/boosts/mirror_small.bmp')

        BoostMixin.__init__(self, screen, base_dir, config, 'mirror', life)

    def activate(self):
        self.is_active = True
        self.plate.rect.y += 24
        self.plate.flip = True

    def deactivate(self):
        self.plate.flip = False


class Score:
    def __init__(self, screen, base_dir, msg):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.msg = msg
        self.color = (255, 255, 255)
        self.font = pygame.font.Font(f'{base_dir}/assets/fonts/pixeboy.ttf', 22)

        self.img = self.font.render(self.msg, True, self.color)
        self.rect = self.img.get_rect()

        self.rect.top = self.screen_rect.top + 2
        self.rect.right = self.screen_rect.right - 2

    def update(self):
        self.img = self.font.render(self.msg, True, self.color)
        self.rect = self.img.get_rect()

        self.rect.top = self.screen_rect.top + 2
        self.rect.right = self.screen_rect.right - 2

    def blit(self):
        self.screen.blit(self.img, self.rect)


class EndCaption(CaptionMixin):
    def __init__(self, screen, base_dir, config):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.score = 0

        CaptionMixin.__init__(self, base_dir, config, 'Your score: {0}')

    def update(self):
        CaptionMixin.update(self, self.score)

    def locate(self):
        self.rect.centerx = self.screen_rect.centerx
        self.rect.y = 125


class PauseCaption(CaptionMixin):
    def __init__(self, screen, base_dir, config):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        CaptionMixin.__init__(self, base_dir, config, 'Pause')

    def locate(self):
        self.rect.centerx = self.screen_rect.centerx
        self.rect.y = 125


class ResumeButton(SceneButtonMixin, pygame.sprite.Sprite):
    def __init__(self, screen, base_dir, config):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.width = self.height = 63

        self.img = pygame.image.load(f'{base_dir}/assets/images/buttons/resume.bmp')
        self.rect = self.img.get_rect()

        SceneButtonMixin.__init__(self, base_dir, config, 'game', 'pause', 'game', 'game', 0)


class PauseLobbyButton(SceneButtonMixin):
    def __init__(self, screen, base_dir, config, defeat, *defeat_args):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.width = self.height = 63

        self.img = pygame.image.load(f'{base_dir}/assets/images/buttons/lobby.bmp')
        self.rect = self.img.get_rect()

        self.defeat = defeat
        self.defeat_args = defeat_args

        SceneButtonMixin.__init__(self, base_dir, config, 'game', 'pause', 'lobby', 'lobby', 0)

    def press(self):
        self.defeat(*self.defeat_args)
        self.config['scene'] = 'game'
        self.config['sub_scene'] = 'pause'
        self.leave(self.change_scene)


class AgainButton(SceneButtonMixin):
    def __init__(self, screen, base_dir, config):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.width = self.height = 63

        self.img = pygame.image.load(f'{base_dir}/assets/images/buttons/again.bmp')
        self.rect = self.img.get_rect()

        SceneButtonMixin.__init__(self, base_dir, config, 'game', 'end', 'game', 'game', 0)


class EndLobbyButton(SceneButtonMixin):
    def __init__(self, screen, base_dir, config):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.width = self.height = 63

        self.img = pygame.image.load(f'{base_dir}/assets/images/buttons/lobby.bmp')
        self.rect = self.img.get_rect()

        SceneButtonMixin.__init__(self, base_dir, config, 'game', 'end', 'lobby', 'lobby', 0)
