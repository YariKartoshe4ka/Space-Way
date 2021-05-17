import pygame


class Text:
    def __init__(self, screen, base_dir, msg):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.msg = msg
        self.color = (255, 255, 255)
        self.font = pygame.font.Font(f'{base_dir}/assets/fonts/pixeboy.ttf', 70)

        self.img = self.font.render(self.msg, True, self.color)
        self.rect = self.img.get_rect()

        self.rect.center = self.screen_rect.center

    def update(self):
        self.img = self.font.render(self.msg, True, self.color)
        self.rect = self.img.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery

    def blit(self):
        self.screen.blit(self.img, self.rect)
