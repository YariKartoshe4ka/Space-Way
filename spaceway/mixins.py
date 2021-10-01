""" File with implementations of various mixins for easier creation of
    objects and following the DRY principle  """

from typing import Union
from random import randint

import pygame

from .collection import SceneButtonsGroup
from .rect import FloatRect


class SceneButtonMixin(pygame.sprite.Sprite):
    """ Mixin for scene buttons, which can change current scene """

    def __init__(self, base_dir, config, scene: str, sub_scene: str,
                 change_scene_to: str, change_sub_scene_to: str, speed: int = 0,
                 action: Union['enter', 'leave', 'stop'] = 'stop') -> None:
        """ Initialize the mixin anywhere in your `__init__` function. `scene`
            and `sub_scene` arguments determine which scene button belongs to.
            `change_scene_to` and `change_sub_scene_to` determine which scene
            will be changed when the button is clicked. `speed` argument
            defines speed of button movement. `action` argument defines first
            action of button """
        pygame.sprite.Sprite.__init__(self)

        # Set variables for next use
        self.config = config
        self.action = action

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
                self.rect.y += (self.speed if self.action == 'leave' else -self.speed) * self.config['ns'].dt
            else:
                # Else, stop button and call action callback
                if self.action == 'enter':
                    self.post_enter()
                else:
                    self.post_leave()
                self.action = 'stop'

    def blit(self) -> None:
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
        """ Change scene to another one (that was defined in `__init__`) """
        self.config['scene'] = self.change_scene_to
        self.config['sub_scene'] = self.change_sub_scene_to

    def press(self) -> None:
        """ Сallback of button that is performed when it is pressed """

        # Find `SceneButtonsGroup` button belongs to
        for group in self.groups():
            if isinstance(group, SceneButtonsGroup):
                # Leave buttons of current scene, and enter of next
                group.leave_buttons()
                group.enter_buttons(self.change_scene_to, self.change_sub_scene_to)
                break

        self.leave(self.change_scene)


class CaptionMixin:
    """ Mixin for more convenient header creation.
        Automatically selects color of border for caption """

    def __init__(self, base_dir, config, caption: str) -> None:
        """ Initializing the mixin. if you redefine the `__init__` function
            call the `__init__` function of `CaptionMixin at the end of
            your `__init__` function. Pass `caption` argument with text
            of caption (it also can be a format string) """

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

    def update(self, *fields) -> None:
        """ Update image (text) of caption and its border. Note that
            this function will recreate `rect` and previous position
            will be deleted (overwritten). Define `locate` function
            to update `rect` position. if you redefine this function,
            it must be called inside your function anywhere. Pass
            arguments for caption, if `caption` is format string """

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

    def blit(self) -> None:
        """ Blit of caption in two steps: border, then text. """

        # Creating border: text of selected color is drawn with indents
        # (size of border) in four directions: up, right, down, and left
        self.screen.blit(self.colors[self.config['user']['color']], (self.rect.x + self.border, self.rect.y))
        self.screen.blit(self.colors[self.config['user']['color']], (self.rect.x - self.border, self.rect.y))
        self.screen.blit(self.colors[self.config['user']['color']], (self.rect.x, self.rect.y + self.border))
        self.screen.blit(self.colors[self.config['user']['color']], (self.rect.x, self.rect.y - self.border))

        # Text of main color is drawn in the center (over the top)
        self.screen.blit(self.img, self.rect)

    def locate(self) -> None:
        """ Change `rect` position. If you don't override this function,
            caption will be located in the upper corner """
        pass


class SettingsButtonMixin(pygame.sprite.Sprite):
    """ Mixin for creating settings buttons. Simplifies the work by
        automatically changing the state and image of the button """

    def __init__(self, screen, config, config_index: str) -> None:
        """ Intialize mixin at the end of your `__init__` function.
            Pass `config_index` argument, which means the key in the
            configuration (config['user'][config_index]). Also define
            an `imgs` dictionary with images for a specific state, e.g.:

                self.imgs = {state1: pygame.Surface, state2: pygame.Surface ...} """

        pygame.sprite.Sprite.__init__(self)

        # Setting variables for the further use
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.config = config
        self.config_index = config_index

        # Getting state from configuration by `config_index`
        self.state = self.config['user'][self.config_index]

        # Setting image by current state and getting its rectangle
        self.img = self.imgs[self.state]
        self.rect = self.img.get_rect()

    def change_state(self) -> None:
        """ Changes state of button. By default it has on-off behaviour """
        self.state = not self.state

    def update(self) -> None:
        """ Update button: synchronize image and configuration with button state """
        self.img = self.imgs[self.state]
        self.config['user'][self.config_index] = self.state

    def blit(self) -> None:
        """ Blit button """
        self.screen.blit(self.img, self.rect)

    def press(self) -> None:
        """ Press callback of button. Changes self state and updates itself """
        self.change_state()
        self.update()


class BoostMixin:
    """ Mixin for easier creation of boosts """

    def __init__(self, screen, base_dir, config, name: str, life: int) -> None:
        """ Initialize of boost. Initialize it at the end of your `__init__`
            function. Pass `name` to define name of boost. Pass `life` to
            define lifetime of your boost (in seconds). Previously define
            `img_idle` (float image that is displayed before activation) and
            `img_small` (displayed in the upper-left corner after activation) """

        # Setting `screen` for the further use
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        # Setting `config` for the further use
        self.config = config

        # Color of time left when there is a lot of time left
        self.fg_color = (255, 255, 255)

        # Color of time left when there is little time left
        self.bg_color = (255, 0, 0)

        # Setting `font` for the further use
        self.font = pygame.font.Font(f'{base_dir}/assets/fonts/pixeboy.ttf', 28)

        # Setting variables for the further use
        self.name = name
        self.life = life
        self.is_active = False
        self.tick = 0

        # Generating a rectangle of `img_idle` and randomly positioning it
        self.rect_idle = FloatRect(self.img_idle.get_rect())
        self.rect_idle.y = randint(self.screen_rect.top, self.screen_rect.bottom - self.rect_idle.height - 2)
        self.rect_idle.left = self.screen_rect.right

        self.rect = self.rect_idle

        # Generating a rectangle of `img_small` and positioning it at the upper-left corner
        self.rect_small = self.img_small.get_rect()
        self.rect_small.left = self.screen_rect.left + 2

    def update(self) -> None:
        """ Updates boost """

        # If boost was activated
        if self.is_active:
            # Vertical positioning of boost, taking into account the number in the boost queue
            self.rect_small.top = self.screen_rect.top + 2 * self.number_in_queue + 18 * (self.number_in_queue - 1)

            # Generating text with the remaining lifetime
            if (self.life * self.config['FPS'] - self.tick) // self.config['FPS'] + 1 <= 3:
                # Rendering text using `bg_border`, if there is little time left
                self.img_life = self.font.render(f"{(self.life * self.config['FPS'] - self.tick) // self.config['FPS'] + 1}S", True, self.bg_color)
                self.rect_life = self.img_life.get_rect()
                self.rect_life.top = self.screen_rect.top + 2 * self.number_in_queue + 18 * (self.number_in_queue - 1)
                self.rect_life.left = self.screen_rect.left + 24
            else:
                # Rendering text using `fg_border`, if there is a lot of time left
                self.img_life = self.font.render(f"{(self.life * self.config['FPS'] - self.tick) // self.config['FPS'] + 1}S", True, self.fg_color)
                self.rect_life = self.img_life.get_rect()
                self.rect_life.top = self.screen_rect.top + 2 * self.number_in_queue + 18 * (self.number_in_queue - 1)
                self.rect_life.left = self.screen_rect.left + 24

            if self.life * self.config['FPS'] - self.tick <= 0:
                # Deactivate and kill the boost if there is no time left
                self.deactivate()
                self.kill()
            else:
                # Continue count life time if there is a lot of time left
                self.tick += 1
        else:
            # Continue movement of boost if it has not activated yet
            self.rect_idle.x -= self.config['ns'].speed * self.config['ns'].dt

        # Kill boost if it has left the screen
        if self.rect_idle.right < 0:
            self.kill()

    def blit(self) -> None:
        """ Blit boost """
        if self.is_active:
            # If boost was activated, blit small and time left images
            self.screen.blit(self.img_life, self.rect_life)
            self.screen.blit(self.img_small, self.rect_small)
        else:
            # If boost was not activated, blit idle image
            self.screen.blit(self.img_idle, self.rect_idle)

    def activate(self) -> None:
        """ Сallback that is called when the boost is activated. Do
            not forget to call this if you redefine it in your boost """

        # Activate boost
        self.is_active = True

    def deactivate(self) -> None:
        """ Callback that is called when the boost is deactivated """
        pass
