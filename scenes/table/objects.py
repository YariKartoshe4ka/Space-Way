import pygame


pygame.font.init()


class TableScore:
    def __init__(self, screen, base_dir, msg=['Score table']):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.msg = msg

        self.width = 250
        self.height = 100
        self.fg_color = (255, 255, 255)
        self.bg_color = (0, 0, 0)
        self.font = pygame.font.Font(f'{base_dir}/assets/fonts/pixeboy.ttf', 36) 

        self._rect = pygame.Rect(0, 0, self.width, self.height)
        self._rect.center = self.screen_rect.center

        self.imgs = []
        self.rects = []

        self.update()

    def update(self):
        y = 100

        for line in self.msg:
            img = self.font.render(line, True, self.fg_color, self.bg_color)
            self.imgs.append(img)
            rect = img.get_rect()
            rect.centerx = self.screen_rect.centerx
            rect.y = y
            self.rects.append(rect)

            y += 25
            if line == 'Score table':
                y += 25


    def blit(self):
        for i in range(len(self.msg)):
            self.screen.blit(self.imgs[i], self.rects[i])
        
        self.imgs = []
        self.rects = []