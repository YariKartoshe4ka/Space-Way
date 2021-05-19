from json import dump

import pygame


class SceneButtonMixin:
    """ Mixin of button """

    def __init__(self, screen, base_dir, config, scene, sub_scene):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.config = config

        self.rect = self.img.get_rect()

        self.scene = scene
        self.sub_scene = sub_scene

    def blit(self):
        self.screen.blit(self.img, self.rect)

    def change_scene(self):
        self.config['scene'] = self.scene
        self.config['sub_scene'] = self.sub_scene

    def on_press(self):
        self.change_scene()


class ButtonMixin:
    def __init__(self, screen, base_dir, config, switch):
        self.switch = switch

        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.config = config

        self.settings_path = f'{base_dir}/config/user.json'

        if self.switch:
            self.state = self.config['user'][self.index]
            self.change_image()

        self.rect = self.img.get_rect()

        self.rect.center = self.screen_rect.center

        self._screen = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self._screen.fill((0, 0, 0, 0))

        self._rect = pygame.Rect(0, 0, self.width, self.height)
        self._rect.center = self.rect.center

        self.is_save = False

    def update(self):
        if self.is_save and self.switch:
            with open(self.settings_path, 'w') as file:
                dump(self.config['user'], file, indent=4)

            self.is_save = False

        if self.switch:
            self.state = self.config['user'][self.index]
            self.change_image()

        self._rect.center = self.rect.center

    def blit(self):
        self.screen.blit(self._screen, self.rect)
        self.screen.blit(self.img, self.rect)
        self._screen.fill((0, 0, 0, 0), self._rect, pygame.BLEND_RGBA_ADD)

    def change_image(self):
        if self.state:
            self.img = self.imgs['true']
        else:
            self.img = self.imgs['false']


class FloatButtonMixin:
    def __init__(self, base_dir, config, direction):
        self.config = config

        self._screen = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self._screen.fill((0, 0, 0, 0))

        self._rect = pygame.Rect(0, 0, self.width, self.height)
        self._rect.centerx = self.rect.centerx
        self._rect.centery = self.rect.centery

        self.direction = direction

        if direction == 'top':
            self.to_bottom = True
            self.to_top = False
            self.change_scene = False

        elif direction == 'bottom':
            self.to_bottom = False
            self.to_top = True
            self.change_scene = False

    def update(self):
        if self.direction == 'top':
            if self.to_top:
                if self.rect.bottom >= self.screen_rect.top:
                    self.rect.y -= self.speed
                else:
                    self.to_top = False

                    if self.change_scene:
                        self.change_scene = False
                        self.config['scene'] = self.scene

            elif self.to_bottom:
                if self.rect.centery <= self.screen_rect.centery:
                    self.rect.y += self.speed
                else:
                    self.to_bottom = False

        elif self.direction == 'bottom':
            if self.to_bottom:
                if self.rect.top <= self.screen_rect.bottom:
                    self.rect.y += self.speed
                else:
                    self.to_bottom = False

                    if self.change_scene:
                        self.change_scene = False
                        self.config['scene'] = self.scene

            elif self.to_top:
                if self.rect.bottom + 5 >= self.screen_rect.bottom:
                    self.rect.y -= self.speed
                else:
                    self.to_top = False

        self._rect.center = self.rect.center

    def blit(self):
        self.screen.blit(self._screen, self.rect)
        self.screen.blit(self.img, self.rect)
        self._screen.fill((0, 0, 0, 0), self._rect, pygame.BLEND_RGBA_ADD)


class CaptionMixin:
    """ Mixin for more convenient header creation.
        Automatically selects color of border for caption. """

    def __init__(self, base_dir, config, caption):
        """ Initializing the mixin. if you redefine the `__init__` function
            call the `__init__` function of `CaptionMixin at the end of
            your `__init__` function """

        # Setting variables for later use
        self.config = config
        self.caption = caption

        # Setting color for text
        self.fg_color = (255, 255, 255)

        # Setting width of border (px)
        self.border = 1

        # Setting font for later generating image of text
        self.font = pygame.font.Font(f'{base_dir}/assets/fonts/pixeboy.ttf', 72)

        # Calling `update` function for generating all images
        self.update()

    def update(self, *fields):
        """ Update image (text) of caption and its border. Note that
            this function will recreate `rect` and previous position
            will be deleted (overwritten). Define `locate` function
            to update `rect` position. if you redefine this function,
            it must be called inside your function anywhere """

        # Render text of caption
        self.img = self.font.render(self.caption.format(*fields), True, self.fg_color)

        # Render borders of different colors
        self.colors = [self.font.render(self.caption.format(*fields), True, (0, 153, 255)),
                       self.font.render(self.caption.format(*fields), True, (252, 15, 192)),
                       self.font.render(self.caption.format(*fields), True, (0, 255, 0))]

        # Recreate rect of text
        self.rect = self.img.get_rect()

        # Locate rect of text
        self.locate()

    def blit(self):
        """ Blit of caption in two steps: border, then text. """

        # Creating border: text of selected color is drawn with indents
        # (size of border) in four directions: up, right, down, and left
        self.screen.blit(self.colors[self.config['user']['color']], (self.rect.x + self.border, self.rect.y))
        self.screen.blit(self.colors[self.config['user']['color']], (self.rect.x - self.border, self.rect.y))
        self.screen.blit(self.colors[self.config['user']['color']], (self.rect.x, self.rect.y + self.border))
        self.screen.blit(self.colors[self.config['user']['color']], (self.rect.x, self.rect.y - self.border))

        # Text of main color is drawn in the center (over the top) 
        self.screen.blit(self.img, self.rect)

    def locate(self):
        """ Change `rect` position. If you don't override this function caption
            will be located in the upper corner (x: 0, y: 0) """
        pass


class BoostMixin:
    def __init__(self, base_dir, config):
        self.config = config

        self.fg_color = (255, 255, 255)
        self.bg_color = (255, 0, 0)
        self.font = pygame.font.Font(f'{base_dir}/assets/fonts/pixeboy.ttf', 28)

        self.is_active = False
        self.tick = 0

        self.rect_3 = self.img_3.get_rect()
        self.rect_3.left = self.screen_rect.left + 2

    def _update(self):
        if self.is_active:
            self.rect_3.top = self.screen_rect.top + 2 * self.number_in_queue + 18 * (self.number_in_queue - 1)
            if (self.life * self.config['FPS'] - self.tick) // self.config['FPS'] + 1 <= 3:
                self.img_2 = self.font.render(f"{(self.life * self.config['FPS'] - self.tick) // self.config['FPS'] + 1}S", True, self.bg_color)
                self.rect_2 = self.img_2.get_rect()
                self.rect_2.top = self.screen_rect.top + 2 * self.number_in_queue + 18 * (self.number_in_queue - 1)
                self.rect_2.left = self.screen_rect.left + 24
            else:
                self.img_2 = self.font.render(f"{(self.life * self.config['FPS'] - self.tick) // self.config['FPS'] + 1}S", True, self.fg_color)
                self.rect_2 = self.img_2.get_rect()
                self.rect_2.top = self.screen_rect.top + 2 * self.number_in_queue + 18 * (self.number_in_queue - 1)
                self.rect_2.left = self.screen_rect.left + 24

            if self.life * self.config['FPS'] - self.tick <= 0:
                self.deactivate()
                self.kill()
            else:
                self.tick += 1
        else:
            self.rect.x -= self.config['speed']

        if self.rect.right < 0:
            self.kill()

    def _blit(self):
        if self.is_active:
            self.screen.blit(self.img_2, self.rect_2)
            self.screen.blit(self.img_3, self.rect_3)
        else:
            self.screen.blit(self.img, self.rect)

    def update(self):
        self._update()

    def blit(self):
        self._blit()

    def activate(self):
        self.is_active = True

    def deactivate(self):
        pass


