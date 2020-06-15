import pygame
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
    def __init__(self, screen, base_dir, config):
        super().__init__()

        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.config = config

        self.img_idle = pygame.image.load(f'{base_dir}/assets/images/plate/idle.bmp')
        self.img_fly = pygame.image.load(f'{base_dir}/assets/images/plate/fly.bmp')

        self.img = self.img_idle
        self.rect = self.img.get_rect()

        self.rect.x = 5
        self.rect.centery = self.screen_rect.centery

        self.gravity = 7

        self.is_jump = False
        self.jump = 10
        self.sounds = {'jump': f'{base_dir}/assets/sounds/jump.wav',
                       'bang': f'{base_dir}/assets/sounds/bang.wav',
                       'score': f'{base_dir}/assets/sounds/score.wav'}

    def reset(self):
        self.rect.centery = self.screen_rect.centery
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

        self.is_bang = False
        self.bang = 0


    def blit(self):
        self.screen.blit(self.img, self.rect)

    def update(self):
        self.rect.x -= self.config['speed']


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


class End:
    def __init__(self, screen, base_dir, config):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.config = config

        self.fg_color = (255, 255, 255)
        self.bg_color = (0, 153, 255)
        self.font = pygame.font.Font(f'{base_dir}/assets/fonts/pixeboy.ttf', 60)
        self.border = 1

        self._screen = pygame.Surface((self.config['mode']), pygame.SRCALPHA)

        self._rect = pygame.Rect(0, 0, self.config['mode'][0], self.config['mode'][1])
        self._rect.x = 0
        self._rect.y = 0

        self.buttons = pygame.sprite.Group()
        self.buttons.add(LobbyButton(screen, base_dir))
        self.buttons.add(AgainButton(screen, base_dir))

    def update(self):
        self.img_fg = self.font.render(f"Your score: {self.config['score']}", True, self.fg_color)
        self.img_bg = self.font.render(f"Your score: {self.config['score']}", True, self.bg_color)
        self.rect = self.img_fg.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.y = 125

        width = 63
        space = 7
        x = (self.config['mode'][0] - (len(self.buttons) * width + (len(self.buttons) - 1) * space)) // 2
        
        for button in self.buttons.sprites():
            button.rect.x = x
            button.update()
            x += width + space

    def blit(self):
        self.screen.blit(self._screen, self._rect)
        self._screen.fill((0, 0, 0, 0))
        self.screen.blit(self.img_bg, (self.rect.x + self.border, self.rect.y))
        self.screen.blit(self.img_bg, (self.rect.x - self.border, self.rect.y))
        self.screen.blit(self.img_bg, (self.rect.x, self.rect.y + self.border))
        self.screen.blit(self.img_bg, (self.rect.x, self.rect.y - self.border))
        self.screen.blit(self.img_fg, self.rect)

        for button in self.buttons.sprites(): button.blit()


class LobbyButton(pygame.sprite.Sprite):
    def __init__(self, screen, base_dir):
        super().__init__()

        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.width = self.height = 63

        self.img_idle = pygame.image.load(f'{base_dir}/assets/images/buttons/lobby.bmp')
        self.img = self.img_idle
        self.rect = self.img.get_rect()

        self.rect.center = self.screen_rect.center

        self._screen = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self._screen.fill((0, 0, 0, 0))

        self._rect = pygame.Rect(0, 0, self.width, self.height)
        self._rect.center = self.rect.center

    def update(self):
        self._rect.center = self.rect.center

    def blit(self):
        self.screen.blit(self._screen, self.rect)
        self.screen.blit(self.img, self.rect)
        self._screen.fill((0, 0, 0, 0), self._rect, pygame.BLEND_RGBA_ADD)


class AgainButton(pygame.sprite.Sprite):
    def __init__(self, screen, base_dir):
        super().__init__()

        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.width = self.height = 63

        self.img_idle = pygame.image.load(f'{base_dir}/assets/images/buttons/again.bmp')
        self.img = self.img_idle
        self.rect = self.img.get_rect()

        self.rect.center = self.screen_rect.center

        self._screen = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self._screen.fill((0, 0, 0, 0))

        self._rect = pygame.Rect(0, 0, self.width, self.height)
        self._rect.center = self.rect.center

    def update(self):
        self._rect.center = self.rect.center

    def blit(self):
        self.screen.blit(self._screen, self.rect)
        self.screen.blit(self.img, self.rect)
        self._screen.fill((0, 0, 0, 0), self._rect, pygame.BLEND_RGBA_ADD)


class Pause:
    def __init__(self, screen, base_dir, config):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.config = config

        self.fg_color = (255, 255, 255)
        self.bg_color = (0, 153, 255)
        self.font = pygame.font.Font(f'{base_dir}/assets/fonts/pixeboy.ttf', 60)
        self.border = 1

        self.img_fg = self.font.render('Pause', True, self.fg_color)
        self.img_bg = self.font.render('Pause', True, self.bg_color)
        self.rect = self.img_fg.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.y = 125

        self._screen = pygame.Surface((self.config['mode']), pygame.SRCALPHA)

        self._rect = pygame.Rect(0, 0, self.config['mode'][0], self.config['mode'][1])
        self._rect.x = 0
        self._rect.y = 0

        self.buttons = pygame.sprite.Group()
        self.buttons.add(LobbyButton(screen, base_dir))
        self.buttons.add(ResumeButton(screen, base_dir))

    def update(self):
        width = 63
        space = 7
        x = (self.config['mode'][0] - (len(self.buttons) * width + (len(self.buttons) - 1) * space)) // 2
        
        for button in self.buttons.sprites():
            button.rect.x = x
            button.update()
            x += width + space

    def blit(self):
        self.screen.blit(self._screen, self._rect)
        self._screen.fill((0, 0, 0, 0))
        self.screen.blit(self.img_bg, (self.rect.x + self.border, self.rect.y))
        self.screen.blit(self.img_bg, (self.rect.x - self.border, self.rect.y))
        self.screen.blit(self.img_bg, (self.rect.x, self.rect.y + self.border))
        self.screen.blit(self.img_bg, (self.rect.x, self.rect.y - self.border))
        self.screen.blit(self.img_fg, self.rect)

        for button in self.buttons.sprites(): button.blit()


class ResumeButton(pygame.sprite.Sprite):
    def __init__(self, screen, base_dir):
        super().__init__()

        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.width = self.height = 63

        self.img_idle = pygame.image.load(f'{base_dir}/assets/images/buttons/resume.bmp')
        self.img = self.img_idle
        self.rect = self.img.get_rect()

        self.rect.center = self.screen_rect.center

        self._screen = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self._screen.fill((0, 0, 0, 0))

        self._rect = pygame.Rect(0, 0, self.width, self.height)
        self._rect.center = self.rect.center

    def update(self):
        self._rect.center = self.rect.center

    def blit(self):
        self.screen.blit(self._screen, self.rect)
        self.screen.blit(self.img, self.rect)
        self._screen.fill((0, 0, 0, 0), self._rect, pygame.BLEND_RGBA_ADD)
