""" File with implementations of additional data structures """

import pygame


class BoostsGroup(pygame.sprite.Group):
    """ Extension of default pygame.sprite.Group for more easier control
        of boosts. Boosts are stored in two groups: active (which were
        activated) and passive (which were not activated). Active group
        cannot contain more than one boost of one type. Boosts are stored
        in form name-boost:

            {'time': <TimeBoost sprite(in 1 groups)>}

        Passive group contains other boosts in spritedict-likely style
        (boost-None):

            {<ShieldBoost sprite(in 1 groups)>: 0} """

    active = {}
    passive = {}
    next_spawn = 1

    def add_internal(self, boost):
        """ Adds boost to passive group """

        self.passive[boost] = 0
        pygame.sprite.Group.add_internal(self, boost)

    def remove_internal(self, boost):
        """ Removes boost. If boost is located in passive group,
            it simply will remove it from group. If boost is located
            in active group, it will update number in queue of other
            boosts and remove boost from group """

        if self.get(boost.name) == boost:
            flag = False

            for name, item in self.active.items():
                if name == boost.name:
                    flag = True

                elif flag:
                    item.number_in_queue -= 1

            del self.active[boost.name]
            pygame.sprite.Group.remove_internal(self, boost)

        elif self.passive.get(boost) == 0:
            del self.passive[boost]
            pygame.sprite.Group.remove_internal(self, boost)

    def empty(self):
        """ Resets itself """

        pygame.sprite.Group.empty(self)
        self.active.clear()
        self.passive.clear()
        self.next_spawn = 3

    def __contains__(self, item):
        """ Will return True, if group contains activated
            boost with passed name, else - False """

        if item.__class__.__name__ == 'str':
            return bool(self.get(item))
        return self.has(item)

    def activate(self, boost):
        """ Activates passed boost and move boost from passive group
            to active. If boost with boost's name have already activated,
            it will nullify tick (boost timer will start again) """

        boost.number_in_queue = len(self.active) + 1

        if self.active.get(boost.name):
            self.active[boost.name].tick = 0
            self.remove_internal(boost)
        else:
            del self.passive[boost]
            self.active[boost.name] = boost
            boost.activate()

    def get(self, name):
        """ Will return boost if active group contains boost
            with passed name. Else it will return None """

        return self.active.get(name)


class CenteredButtonsGroup(pygame.sprite.Group):
    """ Extension of pygame.sprite.Group for centering group of
        buttons on screen. Requires an additional parameter during
        initialization `mode` (list or tuple with sizes of screen).
        When you add or remove buttons, the group is centered again """

    def __init__(self, mode: list, *buttons):
        """ Initialization of group: adding buttons and setting
            of width and height of screen """

        pygame.sprite.Group.__init__(self, *buttons)
        self.screen_width, self.screen_height = mode

    def center(self):
        """ Centering of group """

        space = 7
        buttons_width = 0

        for button in self:
            buttons_width += button.width

        all_width = buttons_width + space * (len(self) - 1)
        x = (self.screen_width - all_width) // 2

        for button in self:
            button.rect.x = x
            button.rect.centery = self.screen_height // 2

            x += button.width + space

    def perform_point_collides(self, point: tuple) -> bool:
        for button in self:
            if button.rect.collidepoint(point):
                button.press()
                return True
        return False

    def add_internal(self, button):
        """ Adding button and centering of group """

        pygame.sprite.Group.add_internal(self, button)
        self.center()

    def remove_internal(self, button):
        """ Removing button and centering of group """

        pygame.sprite.Group.remove_internal(self, button)
        self.center()

    def draw(self):
        for button in self:
            button.update()
            button.blit()


class SceneButtonsGroup(pygame.sprite.Group):
    buttons: dict = {}

    def __init__(self, config, *args):
        pygame.sprite.Group.__init__(self, *args)

        self.config = config

    def add_internal(self, button) -> None:
        if self.buttons.get(button.scene) is None:
            self.buttons[button.scene] = dict()

        if self.buttons[button.scene].get(button.sub_scene) is None:
            self.buttons[button.scene][button.sub_scene] = list()

        self.buttons[button.scene][button.sub_scene].append(button)

        pygame.sprite.Group.add_internal(self, button)

    def remove_internal(self, button) -> None:
        self.buttons[button.scene][button.sub_scene].remove(button)

        pygame.sprite.Group.remove_internal(self, button)

    def perform_point_collides(self, point: tuple) -> bool:
        for button in self.get_by_scene():
            if button.rect.collidepoint(point):
                self.leave_buttons(self.config['scene'], self.config['sub_scene'])
                self.enter_buttons(button.change_scene_to, button.change_sub_scene_to)
                button.press()

                return True
        return False

    def enter_buttons(self, scene: str = '', sub_scene: str = '') -> None:
        for button in self.get_by_scene('' or scene, '' or sub_scene):
            button.enter()

    def leave_buttons(self, scene: str = '', sub_scene: str = '') -> None:
        for button in self.get_by_scene('' or scene, '' or sub_scene):
            button.leave()

    def draw(self) -> None:
        for button in self.get_by_scene():
            button.update()
            button.blit()

    def get_by_scene(self, scene: str = '', sub_scene: str = '') -> list:
        return self.buttons \
            .get(scene or self.config['scene'], {}) \
            .get(sub_scene or self.config['sub_scene'], [])

    def get_by_instance(self, instance: any) -> pygame.sprite.Sprite:
        for button in self:
            if isinstance(button, instance):
                return button

        return None
