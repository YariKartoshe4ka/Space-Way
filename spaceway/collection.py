""" File with implementations of additional data structures """

from typing import Union, List, Tuple, Dict

import pygame


class BoostsGroup(pygame.sprite.Group):
    """ Extension of default pygame.sprite.Group for more easier control
        of boosts. Boosts are stored in two groups: active (which were
        activated) and passive (which were not activated). Active group
        cannot contain more than one boost of one type. Boosts are stored
        in form name-boost:

            {'time': <TimeBoost sprite(in 1 groups)>}

        Passive group contains other boosts in spritedict-likely style
        (boost-0):

            {<ShieldBoost sprite(in 1 groups)>: 0} """

    # Define additional groups
    active: Dict[str, 'BoostMixin'] = {}
    passive: Dict['BoostMixin', int] = {}

    # Define interval for next boost spawn (in score)
    next_spawn = 3

    def add_internal(self, boost: 'BoostMixin') -> None:
        """ Adds boost to passive group """

        self.passive[boost] = 0
        pygame.sprite.Group.add_internal(self, boost)

    def remove_internal(self, boost: 'BoostMixin') -> None:
        """ Removes boost. If boost is located in passive group,
            it simply will remove it from group. If boost is located
            in active group, it will update number in queue of other
            boosts and remove boost from group """

        # If boost was activated
        if self.get(boost.name) == boost:
            # Selected boost was not processed
            flag = False

            for name, item in self.active.items():
                if name == boost.name:
                    # Boost is processed
                    flag = True

                # If boost was processed, update `number_in_queue` of other boosts
                elif flag:
                    item.number_in_queue -= 1

            del self.active[boost.name]
            pygame.sprite.Group.remove_internal(self, boost)

        elif self.passive.get(boost) == 0:
            # If boost was not activated, remove it from passive group
            del self.passive[boost]
            pygame.sprite.Group.remove_internal(self, boost)

    def empty(self) -> None:
        """ Resets itself """

        # Reset default pygame group
        pygame.sprite.Group.empty(self)

        # Reset active and passive groups
        self.active.clear()
        self.passive.clear()

        # Reset `next_spawn`
        self.next_spawn = 3

    def __contains__(self, item: Union[str, 'BoostMixin']) -> bool:
        """ Will return True, if group contains activated
            boost with passed name, else - False """

        if isinstance(item, str):
            return bool(self.get(item))
        return self.has(item)

    def activate(self, boost: 'BoostMixin') -> None:
        """ Activates passed boost and move boost from passive group
            to active. If boost with boost's name have already activated,
            it will nullify tick (boost timer will start again) """

        # Set `number_in_queue` like last boost in queue
        boost.number_in_queue = len(self.active) + 1

        if self.active.get(boost.name):
            # If boost has already activated, zeroize its life time
            self.active[boost.name].tick = 0
            self.remove_internal(boost)
        else:
            # If boost has not activated yet, move it from passive
            # group to active group and activate it
            del self.passive[boost]
            self.active[boost.name] = boost
            boost.activate()

    def get(self, name: str) -> Union['BoostMixin', None]:
        """ Will return boost if active group contains boost
            with passed name. Else it will return `None` """

        return self.active.get(name)


class CenteredButtonsGroup(pygame.sprite.Group):
    """ Extension of pygame.sprite.Group for centering group of
        buttons on screen. Requires an additional parameter during
        initialization `mode` (list or tuple with sizes of screen).
        When you add or remove buttons, the group is centered again.
        For each button, you must specify its dimensions, e.g.:

            self.width = 10
            self.height = 15 """

    # Define space between buttons (px)
    SPACE = 7

    def __init__(self, mode: Tuple[int, int], *buttons: List[pygame.sprite.Sprite]) -> None:
        """ Initialization of group: adding buttons and setting
            of width and height of screen """

        # Initialize inherited group
        pygame.sprite.Group.__init__(self, *buttons)

        # Save mode of screen for the further use
        self.screen_width, self.screen_height = mode

    def center(self) -> None:
        """ Centering of group """

        buttons_width = 0

        # Count width of all buttons
        for button in self:
            buttons_width += button.width

        # Calculate the width of all buttons with spaces between them
        all_width = buttons_width + self.SPACE * (len(self) - 1)

        # Starting point for x
        x = (self.screen_width - all_width) // 2

        # Update rectangles of buttons
        for button in self:
            button.rect.x = x
            button.rect.centery = self.screen_height // 2

            x += button.width + self.SPACE

    def perform_point_collides(self, point: Tuple[int, int]) -> bool:
        """ Detects collisions of buttons with the specified point. If a
            collision was found, it presses on the button and returns `True`,
            otherwise it simply returns `False` """

        # Check all buttons
        for button in self:
            if button.rect.collidepoint(point):
                # If collision was found, press button and return `True`
                button.press()
                return True

        # Return `False` if no collisions were found
        return False

    def add_internal(self, button: pygame.sprite.Sprite) -> None:
        """ Adding button and centering of group """

        pygame.sprite.Group.add_internal(self, button)
        self.center()

    def remove_internal(self, button: pygame.sprite.Sprite) -> None:
        """ Removing button and centering of group """

        pygame.sprite.Group.remove_internal(self, button)
        self.center()

    def draw(self) -> None:
        """ Updates and blits all buttons of group """

        for button in self:
            button.update()
            button.blit()


class SceneButtonsGroup(pygame.sprite.Group):
    """ Extension of pygame.sprite.Group for easier control of
        scenes buttons. It has got dictionary with buttons and
        a structure like this:

            buttons = {
                sceneN: {
                    sub_scene1: [SceneButtonMixin, ...],
                    ...
                    },
                ...
                } """

    # Define an additional dictionary for structuring buttons by scenes
    buttons: Dict[str, Dict[str, List['SceneButtonMixin']]] = {}

    def __init__(self, config, *buttons: List['SceneButtonMixin']) -> None:
        """ Initialization of group. Pass `config` argument and list of buttons
            `buttons` to add them to group """

        # Initialization of inherited group
        pygame.sprite.Group.__init__(self, *buttons)

        # Set `config` for the further use
        self.config = config

    def add_internal(self, button: 'SceneButtonMixin') -> None:
        """ Adding button to group and structuring by scene """

        # If there were not buttons with scene of current button yet
        if self.buttons.get(button.scene) is None:
            self.buttons[button.scene] = dict()

        # If there were not buttons with sub scene of current button yet
        if self.buttons[button.scene].get(button.sub_scene) is None:
            self.buttons[button.scene][button.sub_scene] = list()

        # After checking group structure, we can safely add the button to group
        self.buttons[button.scene][button.sub_scene].append(button)

        pygame.sprite.Group.add_internal(self, button)

    def remove_internal(self, button: 'SceneButtonMixin') -> None:
        """ Remove button from group. It is assumed that button has already been added """

        # Remove button from group
        self.buttons[button.scene][button.sub_scene].remove(button)

        pygame.sprite.Group.remove_internal(self, button)

    def perform_point_collides(self, point: Tuple[int, int]) -> bool:
        """ Detects button collisions with the specified point. If collision
            was found, presses the button, leaves buttons of current scenу
            and enters buttons of scene to which it will be changed """

        # Get all buttons of current scene
        for button in self.get_by_scene():
            # If collision was found
            if button.rect.collidepoint(point):
                # Leave buttons of current scene and enter buttons of next scene
                self.leave_buttons(self.config['scene'], self.config['sub_scene'])
                self.enter_buttons(button.change_scene_to, button.change_sub_scene_to)

                # Press collided button
                button.press()

                return True

        # No collisions were found
        return False

    def enter_buttons(self, scene: str = '', sub_scene: str = '') -> None:
        """ Enters all buttons of selected scene. If no scene was selected,
            buttons of current scene will be entered """

        for button in self.get_by_scene(scene, sub_scene):
            button.enter()

    def leave_buttons(self, scene: str = '', sub_scene: str = '') -> None:
        """ Leaves all buttons of selected scene. If no scene was selected,
            buttons of current scene will be left """

        for button in self.get_by_scene(scene, sub_scene):
            button.leave()

    def draw(self) -> None:
        """ Updates and blits all buttons of group """

        for button in self.get_by_scene():
            button.update()
            button.blit()

    def get_by_scene(self, scene: str = '', sub_scene: str = '') -> List['SceneButtonMixin']:
        """ Returns all buttons of selected scene. If no scene was selected,
            buttons of current scene will be returned """

        return self.buttons \
            .get(scene or self.config['scene'], {}) \
            .get(sub_scene or self.config['sub_scene'], [])

    def get_by_instance(self, instance: any) -> Union['SceneButtonMixin', None]:
        """ Returns only one button or `None` which is an instance of passed class """

        for button in self:
            if isinstance(button, instance):
                # Return button if it is an instance of passed class
                return button

        # Return `None` if no suitable button was found
        return None
