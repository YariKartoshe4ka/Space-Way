import pygame


pygame.font.init()


class TableScore:
    def __init__(self, screen, base_dir, msg=['Score table']):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.base_dir = base_dir

        self.msg = msg

        self.width = 250
        self.height = 100
        self.fg_color = (255, 255, 255)
        self.bg_color = (0, 0, 0)
        self.font = pygame.font.Font(f'{base_dir}/assets/fonts/pixeboy.ttf', 36) 

        self._rect = pygame.Rect(0, 0, self.width, self.height)
        self._rect.center = self.screen_rect.center

        self.border = 1

        self.imgs = []
        self.rects = []

        self.is_update = True

        self.update()

    def update(self):
        if self.is_update:
            with open(f'{self.base_dir}/config/score.csv', 'r') as file:
                data = file.read().split('\n')

            msg = []

            data = sorted(list(map(lambda x: [int(x.split(',')[0]), x.split(',')[1]], data[1:len(data) - 1])))
            data.reverse()

            with open(f'{self.base_dir}/config/score.csv', 'w') as file:
                file.write('score,nick\n')

                for i in data[:5]:
                    msg.append(f'{i[0]} : {i[1]}')
                    file.write(f'{i[0]},{i[1]}\n')

            msg.insert(0, 'Score table')
            self.msg = msg

            y = 100

            for line in self.msg:
                img_fg = self.font.render(line, True, self.fg_color)
                img_bg = self.font.render(line, True, self.bg_color)
                self.imgs.append([img_fg, img_bg])
                rect = img_fg.get_rect()
                rect.centerx = self.screen_rect.centerx
                rect.y = y
                self.rects.append(rect)

                y += 25
                if line == 'Score table':
                    y += 25

                self.is_update = False


    def blit(self):
        for i in range(len(self.msg)):
            self.screen.blit(self.imgs[i][1], (self.rects[i].x + self.border, self.rects[i].y))
            self.screen.blit(self.imgs[i][1], (self.rects[i].x - self.border, self.rects[i].y))
            self.screen.blit(self.imgs[i][1], (self.rects[i].x, self.rects[i].y + self.border))
            self.screen.blit(self.imgs[i][1], (self.rects[i].x, self.rects[i].y - self.border))
            self.screen.blit(self.imgs[i][0], self.rects[i])


class BackButton:
    def __init__(self, screen, base_dir, config):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.width = self.height = 63

        self.config = config

        self.img_idle = pygame.image.load(f'{base_dir}/assets/images/buttons/back.bmp')
        self.img = self.img_idle
        self.rect = self.img.get_rect()

        self.rect.left = self.screen_rect.left + 5
        self.rect.top = self.screen_rect.bottom - 5

        self._screen = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self._screen.fill((0, 0, 0, 0))

        self._rect = pygame.Rect(0, 0, self.width, self.height)
        self._rect.centerx = self.rect.centerx
        self._rect.centery = self.rect.centery

        self.to_bottom = False
        self.to_top = True
        self.change_scene = False

    def update(self):

        if self.to_bottom:
            if self.rect.top <= self.screen_rect.bottom:
                self.rect.y += 4
            else:
                self.to_bottom = False

                if self.change_scene:
                    self.change_scene = False
                    self.config['scene'] = 'lobby'

        elif self.to_top:
            if self.rect.bottom + 5 >= self.screen_rect.bottom:
                self.rect.y -= 4
            else:
                self.to_top = False

        self._rect.center = self.rect.center

    def blit(self):
        self.screen.blit(self._screen, self.rect)
        self.screen.blit(self.img, self.rect)
        self._screen.fill((0, 0, 0, 0), self._rect, pygame.BLEND_RGBA_ADD)
