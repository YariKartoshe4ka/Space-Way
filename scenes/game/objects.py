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
        self.img = self.img_idle

        self.rect = self.img.get_rect()
        self.rect.y = randint(1, config['mode'][1] - 56)
        self.rect.left = self.screen_rect.right

    def blit(self):
        self.screen.blit(self.img, self.rect)

    def update(self):
        self.speed = self.config['level'] * 10
        self.rect.x -= self.speed
