""" File with implementations of additional data structures """

from typing import List, Dict

import pygame


class BoostsGroup(pygame.sprite.Group):
    """Extension of default :group:`pygame.sprite.Group` for more
    easier control of boosts

    Args:
        The same as the pygame :group:`pygame.sprite.Group`

    Note:
        Boosts are stored in two groups: active (which were activated) and passive
        (which weren't activated). Active group cannot contain more than one boost
        of one type, because they are stored in the following format:
        .. code:: python

            {'time': <TimeBoost sprite(in 1 groups)>}

        Passive group contains other boosts in in the following format:
        .. code:: python

            {<ShieldBoost sprite(in 1 groups)>: 0}
    """

    def __init__(self, *boosts):
        """Constructor method
        """
        # Define additional groups
        self.active: Dict[str, 'BoostMixin'] = {}
        self.passive: Dict['BoostMixin', int] = {}

        # Define interval for next boost spawn (in score)
        self.next_spawn = 3

        # Initialize inherited group
        pygame.sprite.Group.__init__(self, *boosts)

    def add_internal(self, boost) -> None:
        """Adds boost to passive group

        Args:
            boost (spaceway.mixins.BoostMixin): boost to be added to group
        """
        self.passive[boost] = 0
        pygame.sprite.Group.add_internal(self, boost)

    def remove_internal(self, boost) -> None:
        """Removes boost. If boost is located in passive group, it simply will
        remove it from group. If boost is located in active group, it will update
        number in queue of other boosts and then remove boost from group

        Args:
            boost (spaceway.mixins.BoostMixin): Boost to be removed from group
        """
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
        """Resets itself and removes all boosts
        """
        # Reset default pygame group
        pygame.sprite.Group.empty(self)

        # Reset active and passive groups
        self.active.clear()
        self.passive.clear()

        # Reset `next_spawn`
        self.next_spawn = 3

    def __contains__(self, boost):
        """Check if boost contains in this group

        Args:
            boost (Union[str, spaceway.mixins.BoostMixin]): Boost to be checked
                whether it's contained in group. If argument is a string, boost will
                be checked in active group, otherwise among all groups

        Returns:
            bool: Is boost contained in the group or not
        """
        if isinstance(boost, str):
            return bool(self.get(boost))
        return self.has(boost)

    def activate(self, boost) -> None:
        """Activates passed boost and move boost from passive group to active

        Args:
            boost (spaceway.mixins.BoostMixin): Boost to be activated

        Important:
            If some boost with boost's name have already activated, it will nullify
            tick of already activated boost (boost timer will start again)
        """
        # Set `number_in_queue` like last boost in queue
        boost.number_in_queue = len(self.active) + 1

        if self.active.get(boost.name):
            # If boost has already activated, reset its life time
            self.active[boost.name].life = boost.life
            self.remove_internal(boost)
        else:
            # If boost has not activated yet, move it from passive
            # group to active group and activate it
            del self.passive[boost]
            self.active[boost.name] = boost
            boost.activate()

    def get(self, name):
        """Search for a boost with the passed name in active group and,
        if there is one, returns it

        Args:
            name (str): Name of boost

        Returns:
            Union[spaceway.mixins.BoostMixin, None]: Will return boost if
                active group contains it, otherwise `None`
        """
        return self.active.get(name)


class CenteredButtonsGroup(pygame.sprite.Group):
    """Extension of default :group:`pygame.sprite.Group` for centering
    buttons of group on screen

    Args:
        mode (Tuple[int, int]): The size of the :surface:`pygame.Surface`
            relative to which the buttons will be centered
        *buttons (pygame.sprite.Sprite): Buttons to be added to the group

    Note:
        Centering of buttons occurs during the addition/removal of
        a button from a group
    """

    # Define space between buttons (px)
    SPACE = 7

    def __init__(self, mode, *buttons):
        """Constructor method. Adding buttons and setting of width and
        height of surface
        """
        # Save mode of screen for the further use
        self.screen_width, self.screen_height = mode

        # Initialize inherited group
        pygame.sprite.Group.__init__(self, *buttons)

    def center(self) -> None:
        """Centering of group
        """
        buttons_width = 0

        # Count width of all buttons
        for button in self:
            buttons_width += button.rect.w

        # Calculate the width of all buttons with spaces between them
        all_width = buttons_width + self.SPACE * (len(self) - 1)

        # Starting point for x
        x = (self.screen_width - all_width) // 2

        # Update hitboxes of buttons
        for button in self:
            button.rect.x = x
            button.rect.centery = self.screen_height // 2

            x += button.rect.w + self.SPACE

    def perform_point_collides(self, point):
        """Detects collisions of buttons with the specified point. If a
        collision was found, it presses on the button

        Args:
            point (Tuple[int, int]): The point at which the collision is checked

        Returns:
            bool: Has a collision been found
        """
        # Check all buttons
        for button in self:
            if button.rect.collidepoint(point):
                # If collision was found, press button and return `True`
                button.press()
                return True

        # Return `False` if no collisions were found
        return False

    def add_internal(self, button) -> None:
        """Adding button and centering of group

        Args:
            button (pygame.sprite.Sprite): Button to be added to the group
        """
        pygame.sprite.Group.add_internal(self, button)
        self.center()

    def remove_internal(self, button) -> None:
        """Removing button and centering of group

        Args:
            button (pygame.sprite.Sprite): Button to be removed from the group
        """
        pygame.sprite.Group.remove_internal(self, button)
        self.center()

    def draw(self) -> None:
        """Updates and blits all buttons of group
        """
        for button in self:
            button.update()
            button.blit()


class SceneButtonsGroup(pygame.sprite.Group):
    """Extension of default :group:`pygame.sprite.Group` for easier control
    of scene buttons

    Args:
        config (spaceway.config.ConfigManager): The configuration object
        *buttons (pygame.sprite.Sprite): Buttons to be added to the group
    """

    # Define an additional dictionary for structuring buttons by scenes
    buttons: Dict[str, Dict[str, List['SceneButtonMixin']]] = {}

    def __init__(self, config, *buttons):
        """Constructor method
        """
        # Initialization of inherited group
        pygame.sprite.Group.__init__(self, *buttons)

        # Set `config` for the further use
        self.config = config

    def add_internal(self, button) -> None:
        """Adding button to group and structuring by scene

        Args:
            button (pygame.sprite.Sprite): Button to be added to the group
        """
        # If there were not buttons with scene of current button yet
        if self.buttons.get(button.scene) is None:
            self.buttons[button.scene] = dict()

        # If there were not buttons with sub scene of current button yet
        if self.buttons[button.scene].get(button.sub_scene) is None:
            self.buttons[button.scene][button.sub_scene] = list()

        # After checking group structure, we can safely add the button to group
        self.buttons[button.scene][button.sub_scene].append(button)

        pygame.sprite.Group.add_internal(self, button)

    def remove_internal(self, button) -> None:
        """Remove button from group

        Args:
            button (pygame.sprite.Sprite): Button to be removed from the group
        """
        # Remove button from group
        self.buttons[button.scene][button.sub_scene].remove(button)

        pygame.sprite.Group.remove_internal(self, button)

    def perform_point_collides(self, point):
        """Detects collisions of buttons with the specified point. If a collision
        was found, presses the button, leaves buttons of current scene and enters
        buttons of scene to which it will be changed

        Args:
            point (Tuple[int, int]): The point at which the collision is checked

        Returns:
            bool: Has a collision been found
        """
        # Get all buttons of current scene
        for button in self.get_by_scene():
            # If collision was found
            if button.rect.collidepoint(point):
                # Press collided button
                button.press()

                return True

        # No collisions were found
        return False

    def enter_buttons(self, scene='', sub_scene='') -> None:
        """Enters all buttons of passed scene. If no scene was passed,
        buttons of current scene will be entered

        Args:
            scene (Optional[str]): Buttons of specific scene which must be entered
            sub_scene (Optional[str]): Buttons of specific subscene which must be entered
        """
        for button in self.get_by_scene(scene, sub_scene):
            button.enter()

    def leave_buttons(self, scene='', sub_scene='') -> None:
        """Leaves all buttons of passed scene. If no scene was passed,
        buttons of current scene will be left

        Args:
            scene (Optional[str]): Buttons of specific scene which must be left
            sub_scene (Optional[str]): Buttons of specific subscene which must be left
        """
        for button in self.get_by_scene(scene, sub_scene):
            button.leave()

    def draw(self) -> None:
        """Updates and blits buttons current scene
        """
        for button in self.get_by_scene():
            button.update()
            button.blit()

    def get_by_scene(self, scene='', sub_scene=''):
        """Returns all buttons of passed scene. If no scene was selected,
        buttons of current scene will be returned

        Args:
            scene (Optional[str]): Buttons of specific scene which must be returned
            sub_scene (Optional[str]): Buttons of specific subscene which must be returned

        Returns:
            List[pygame.sprite.Sprite]: List of buttons of specific scene
        """
        return self.buttons \
            .get(scene or self.config['scene'], {}) \
            .get(sub_scene or self.config['sub_scene'], [])

    def get_by_instance(self, instance):
        """Returns first button which is an instance of passed class

        Args:
            instance (any): Instance from which button must be inherited

        Returns:
            Union[pygame.sprite.Sprite, None]: Button object, if there is one,
                otherwise `None`
        """
        for button in self:
            if isinstance(button, instance):
                # Return button if it is an instance of passed class
                return button

        # Return `None` if no suitable button was found
        return None
