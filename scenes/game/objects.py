import pygame
from os import getcwd
from random import randint

pygame.font.init()


class Background:
    def __init__(self, screen, base_dir, x, y):
        self.screen = screen

        self.bg = pygame.image.load(f'{base_dir}/assets/images/bg/background.bmp')
        self.rect = self.bg.get_rect()

        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x -= 1

        if self.rect.x <= -840:
            self.rect.x = 0

    def blit(self):
        self.screen.blit(self.bg, self.rect)


class SpacePlate(pygame.sprite.Sprite):
    def __init__(self, screen, base_dir):
        super().__init__()

        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.img_idle = pygame.image.load(f'{base_dir}/assets/images/plate/idle.bmp')
        self.img_fly = pygame.image.load(f'{base_dir}/assets/images/plate/fly.bmp')

        self.img = self.img_idle
        self.rect = self.img.get_rect()

        self.rect.x = 5
        self.rect.centery = self.screen_rect.centery

        self.gravity = 7

        self.is_jump = False
        self.jump = 10   

    def update(self):
        if not self.is_jump:
            self.rect.y += self.gravity
        else:

            if self.jump >= -5:
                if self.jump < 0:
                    self.rect.y += (self.jump ** 2) // 3
                else:
                    self.img = self.img_fly
                    self.rect.y -= (self.jump ** 2) // 3
                self.jump -= 1
            else:
                self.img = self.img_idle
                self.is_jump = False
                self.jump = 10

    def blit(self):
        self.screen.blit(self.img, self.rect)


class Asrteroid(pygame.sprite.Sprite):
    def __init__(self, screen, base_dir, config):
        super().__init__()

        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.config = config

        self.img_idle = pygame.image.load(f'{base_dir}/assets/images/asteroid/idle.bmp')

        self.img_bang = [pygame.image.load(f'{base_dir}/assets/images/asteroid/bang/bang_1.bmp'),
                         pygame.image.load(f'{base_dir}/assets/images/asteroid/bang/bang_2.bmp'),
                         pygame.image.load(f'{base_dir}/assets/images/asteroid/bang/bang_3.bmp'),
                         pygame.image.load(f'{base_dir}/assets/images/asteroid/bang/bang_4.bmp'),
                         pygame.image.load(f'{base_dir}/assets/images/asteroid/bang/bang_5.bmp')]

        self.img = self.img_idle

        self.rect = self.img.get_rect()
        self.rect.y = randint(1, config['mode'][1] - 56)
        self.rect.left = self.screen_rect.right

        self.is_bang = False
        self.bang = 0


    def blit(self):
        self.screen.blit(self.img, self.rect)

    def update(self):
        if self.bang >= 30:
            self.bang = 0
            self.is_bang = False

            return True

        self.speed = self.config['level'] * 10
        self.rect.x -= self.speed

        if self.is_bang:
            self.img = self.img_bang[self.bang // 6]
            self.bang += 1



class Health:
    def __init__(self, screen, base_dir, config):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.config = config

        self.img_zero = pygame.image.load(f'{base_dir}/assets/images/health/zero.bmp')
        self.img_one = pygame.image.load(f'{base_dir}/assets/images/health/one.bmp')
        self.img_two = pygame.image.load(f'{base_dir}/assets/images/health/two.bmp')
        self.img_three = pygame.image.load(f'{base_dir}/assets/images/health/three.bmp')

        self.img = self.img_three

        self.rect = self.img.get_rect()
        self.rect.top = self.screen_rect.top + 2
        self.rect.left = self.screen_rect.left + 2

    def update(self):
        if self.config['health'] == 3:
            self.img = self.img_three
        elif self.config['health'] == 2:
            self.img = self.img_two
        elif self.config['health'] == 1:
            self.img = self.img_one
        else:
            self.img = self.img_zero

    def blit(self):
        self.screen.blit(self.img, self.rect)


class Score:
    def __init__(self, screen, base_dir, msg):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.width = 80
        self.height = 40
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

