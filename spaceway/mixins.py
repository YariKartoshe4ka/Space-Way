from json import dump

import pygame


class SceneButtonMixin(pygame.sprite.Sprite):
    """ Mixin for float buttons. Buttons can only move vertically """

    def __init__(self, base_dir, config, scene: str, sub_scene: str,
                 change_scene_to: str, change_sub_scene_to: str,
                 speed: int = 0, action: str = 'stop'):
        """ Initialize the mixin anywhere in your `__init__` function """
        pygame.sprite.Sprite.__init__(self)

        # Set variables for next use
        self.config = config
        self.action = action if action in ('stop', 'enter', 'leave') else 'stop'

        # If speed is positive, on `enter` event button will move up,
        # on `leave` event - down. If speed is negative, on `enter` event
        # button will move down, on `leave` event - up
        self.speed = speed

        # Set events callbacks
        self.post_enter = lambda: None
        self.post_leave = lambda: None

        # Set scene during which button is displayed
        self.scene = scene
        self.sub_scene = sub_scene

        # Scenes on which will be changed when button will be pressed
        self.change_scene_to = change_scene_to
        self.change_sub_scene_to = change_sub_scene_to

    def update(self) -> None:
        """ Update button position """

        # If button must move
        if self.action != 'stop':
            # Check, if move can be continued
            if self.keep_move():
                # If can be, move button
                self.rect.y += self.speed if self.action == 'leave' else -self.speed
            else:
                # Else, stop button and call action callback
                if self.action == 'enter':
                    self.post_enter()
                else:
                    self.post_leave()
                self.action = 'stop'

    def blit(self):
        """ Blit button """
        self.screen.blit(self.img, self.rect)

    def enter(self, post_enter=lambda: None) -> None:
        """ Start `enter` action and set `post_enter` callback for next use """
        self.action = 'enter'
        self.post_enter = post_enter

    def leave(self, post_leave=lambda: None) -> None:
        """ Start `leave` action and set `post_leave` callback for next use """
        self.action = 'leave'
        self.post_leave = post_leave

    def keep_move(self) -> bool:
        """ Function to control movement of button. It contains
            conditions due of it decides, continue move or not """
        return False

    def change_scene(self) -> None:
        self.config['scene'] = self.change_scene_to
        self.config['sub_scene'] = self.change_sub_scene_to

    def press(self) -> None:
        self.leave(self.change_scene)


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
        """ Change `rect` position. If you don't override this function,
            caption will be located in the upper corner """
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
