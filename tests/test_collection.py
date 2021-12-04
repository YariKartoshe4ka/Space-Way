from random import randint, choice

import pytest

from spaceway.collection import *
from spaceway.mixins import BoostMixin, SceneButtonMixin, SettingsButtonMixin
from spaceway.hitbox import Rect
from utils import *


@pytest.mark.parametrize('boosts_params', [
    [(7, 'a'), (3, 'b'), (5, 'c'), (7, 'a')],
    [(2, 'x'), (2, 'y'), (2, 'z')],
    [(9, 'q'), (3, 'f'), (5, 'r'), (4, 't')]
])
def test_boosts_group(pygame_env, boosts_params):
    screen, base_dir, config, clock = pygame_env

    class TestBoost(BoostMixin):
        def __init__(self, life, name):
            pygame.sprite.Sprite.__init__(self)

            self.img_idle = pygame_surface((30, 30))
            self.img_small = pygame_surface((18, 18), 1)

            BoostMixin.__init__(self, screen, base_dir, config, name, life)

    def create_boosts():
        return [TestBoost(life, name) for life, name in boosts_params]

    def uniq_len(a):
        return len(set(a))

    # Test `add` and `remove` methods of group simply
    test_boosts = create_boosts()
    test_boost = test_boosts[0]
    test_group = BoostsGroup()

    assert len(test_group) == 0

    test_group.add(test_boost)
    assert len(test_group) == 1

    test_group.remove(test_boost)
    assert len(test_group) == 0

    # Test `remove` method for activated boosts
    test_boosts = create_boosts()
    test_group = BoostsGroup(*test_boosts)

    for test_boost in test_boosts:
        test_group.activate(test_boost)

    test_boost = min(test_boosts, key=lambda x: x.number_in_queue)

    assert len(test_group) == uniq_len(boosts_params)

    test_group.remove(test_boost)
    assert len(test_group) == uniq_len(boosts_params) - 1

    # Test `empty` method
    test_boosts = create_boosts()
    test_group = BoostsGroup(*test_boosts)
    test_group.empty()

    assert len(test_group) == len(test_group.active) == len(test_group.passive) == 0
    assert test_group.next_spawn == 3

    # Test `get` method without activated boosts
    test_boosts = create_boosts()
    test_boost = test_boosts[0]
    test_group = BoostsGroup(*test_boosts)

    assert test_group.get(test_boost.name) is None

    # Test `get` method with activated boosts
    test_boosts = create_boosts()
    test_group = BoostsGroup(*test_boosts)

    for test_boost in test_boosts:
        test_group.activate(test_boost)

    test_boost = test_boosts[0]
    assert test_group.get(test_boost.name)

    # Test `__contains__` method
    test_boosts = create_boosts()
    test_group = BoostsGroup(*test_boosts)
    test_boost1, test_boost2 = test_boosts[:2]
    test_group.activate(test_boost1)

    assert test_boost1.name in test_group
    assert test_boost1 in test_group
    assert test_boost2.name not in test_group
    assert test_boost2 in test_group


@pytest.mark.parametrize('buttons_sizes', [
    [(30, 45), (60, 60), (40, 60), (82, 48)],
    [(120, 38), (80, 27), (30, 32), (10, 78)],
    [(74, 52), (33, 48), (20, 12)]
])
def test_centered_buttons_group(pygame_env, buttons_sizes):
    screen, base_dir, config, clock = pygame_env

    class TestSceneButton(SceneButtonMixin):
        def __init__(self, size):
            self.screen = screen
            self.img = pygame_surface(size)
            self.rect = Rect(self.img.get_rect())
            self.rect.topleft = (randint(0, 550), randint(0, 250))
            SceneButtonMixin.__init__(self, base_dir, config, '', '', '', '')

    class TestSettingsButton(SettingsButtonMixin):
        def __init__(self, size):
            self.imgs = {True: pygame_surface(size),
                         False: pygame_surface(size, 1)}

            config_index = rstring(15)
            config['user'][config_index] = True
            SettingsButtonMixin.__init__(self, screen, config, config_index)

            self.rect = Rect(self.img.get_rect())
            self.rect.topleft = (randint(0, 550), randint(0, 250))

    def create_buttons():
        buttons = []
        rects = []

        for button_size in buttons_sizes:
            buttons.append(choice([TestSceneButton, TestSettingsButton])(button_size))
            rects.append(buttons[-1].rect)

        return buttons, rects

    # Test `add` and `remove` methods of group
    test_buttons, buttons_rects = create_buttons()
    test_button = test_buttons[0]
    test_group = CenteredButtonsGroup(config['mode'])

    assert len(test_group) == 0

    test_group.add(test_button)
    assert len(test_group) == 1

    test_group.remove(test_button)
    assert len(test_group) == 0

    # Test centering of buttons which passed to constructor
    test_group = CenteredButtonsGroup(config['mode'], *test_buttons)

    unionall_rect = buttons_rects[0].unionall(buttons_rects[1:])

    assert tuple(map(round, unionall_rect.trunc().center)) == screen.get_rect().center

    # Test centering of buttons which added after group initialization
    test_buttons, buttons_rects = create_buttons()
    test_group = CenteredButtonsGroup(config['mode'])

    test_group.add(test_buttons)
    unionall_rect = buttons_rects[0].unionall(buttons_rects[1:])

    assert tuple(map(round, unionall_rect.trunc().center)) == screen.get_rect().center

    # Remove random button and check if other buttons centered again
    remove_button = choice(test_buttons)

    buttons_rects.remove(remove_button.rect)
    test_group.remove(remove_button)
    unionall_rect = buttons_rects[0].unionall(buttons_rects[1:])

    assert tuple(map(round, unionall_rect.trunc().center)) == screen.get_rect().center

    # Test `draw` method of group
    test_buttons, buttons_rects = create_buttons()
    test_group = CenteredButtonsGroup(config['mode'], *test_buttons)

    @pygame_loop(pygame_env, 1)
    def loop1():
        test_group.draw()

    # Test `perform_point_collides` method of group
    assert test_group.perform_point_collides(test_group.sprites()[0].rect.center)
    assert not test_group.perform_point_collides((-1, -1))


@pytest.mark.parametrize('buttons_scenes', [
    [(1, 1, 2, 2), (3, 3, 1, 1), (2, 2, 1, 1)],
    [('a', 'a', 'b', 'b'), ('b', 'b', 'c', 'c'), ('a', 'a', 'b', 'b')],
    [('abc', 'def', 'asd', 'test'), ('abc', 'def', 'req', 'obr')]
])
def test_scene_buttons_group(pygame_env, buttons_scenes):
    screen, base_dir, config, clock = pygame_env

    class TestSceneButton(SceneButtonMixin):
        def __init__(self, scenes, color):
            self.screen = screen
            self.img = pygame_surface((randint(20, 80), randint(20, 80)), color)
            self.rect = Rect(self.img.get_rect())
            self.rect.topleft = (randint(20, 120), randint(20, 120))
            SceneButtonMixin.__init__(self, base_dir, config, *scenes)

    class UniqueTestInstance:
        pass

    def create_buttons():
        unique_color_scene = buttons_scenes[0][:2]
        buttons = []

        for scenes in buttons_scenes:
            if scenes[:2] == unique_color_scene:
                buttons.append(TestSceneButton(scenes, 0))
            else:
                buttons.append(TestSceneButton(scenes, 1))

        return buttons

    config['scene'], config['sub_scene'] = buttons_scenes[0][:2]

    # Test `draw` method
    test_buttons = create_buttons()
    test_group = SceneButtonsGroup(config, *test_buttons)

    @pygame_loop(pygame_env, 1)
    def loop1():
        test_group.draw()

        assert (
            most_popular_colors(screen, exclude=[(0, 0, 0)])[0] == (0, 57, 255) or
            most_popular_colors(screen, exclude=[(0, 0, 0)])[0] == (255, 46, 222)
        )

    # Test `perform_point_collides` method of group
    assert test_group.perform_point_collides(test_group.sprites()[0].rect.center)
    assert not test_group.perform_point_collides((-1, -1))

    # Test `add` and `remove` methods of group
    test_button = test_buttons[0]
    test_group = SceneButtonsGroup(config)

    assert len(test_group) == 0

    test_group.add(test_button)
    assert len(test_group) == 1

    test_group.remove(test_button)
    assert len(test_group) == 0

    # Test if group with butttons which passed in constructor
    # equals to group with buttons added after initialization
    test_group1 = SceneButtonsGroup(config, *test_buttons)
    test_group2 = SceneButtonsGroup(config)
    test_group2.add(*test_buttons)

    assert len(test_group1) == len(test_group2)

    # Test `get_by_scene` method without parameters
    config['scene'] = buttons_scenes[0][0]
    config['sub_scene'] = buttons_scenes[0][1]

    for test_button in test_group.get_by_scene():
        assert test_button.scene == config['scene']
        assert test_button.sub_scene == config['sub_scene']

    # Test `get_by_scene` method with parameters
    test_group = SceneButtonsGroup(config, *test_buttons)
    scene = buttons_scenes[1][0]
    sub_scene = buttons_scenes[1][1]

    for test_button in test_group.get_by_scene(scene, sub_scene):
        assert test_button.scene == scene
        assert test_button.sub_scene == sub_scene

    # Test `get_by_instance`
    test_group = SceneButtonsGroup(config, *test_buttons)
    assert test_group.get_by_instance(TestSceneButton) == test_buttons[0]
    assert test_group.get_by_instance(UniqueTestInstance) is None

    # Test `enter_buttons` method without parameters
    test_buttons = create_buttons()
    test_group = SceneButtonsGroup(config, *test_buttons)
    config['scene'] = buttons_scenes[0][0]
    config['sub_scene'] = buttons_scenes[0][1]
    test_group.enter_buttons()

    for test_button in test_group:
        if test_button.scene == config['scene'] and test_button.sub_scene == config['sub_scene']:
            assert test_button.action == 'enter'
        else:
            assert test_button.action == 'stop'

    # Test `enter_buttons` method with parameters
    test_buttons = create_buttons()
    test_group = SceneButtonsGroup(config, *test_buttons)
    scene = buttons_scenes[1][0]
    sub_scene = buttons_scenes[1][1]
    test_group.enter_buttons(scene, sub_scene)

    for test_button in test_group:
        if test_button.scene == scene and test_button.sub_scene == sub_scene:
            assert test_button.action == 'enter'
        else:
            assert test_button.action == 'stop'

    # Test `leave_buttons` method without parameters
    test_buttons = create_buttons()
    test_group = SceneButtonsGroup(config, *test_buttons)
    config['scene'] = buttons_scenes[0][0]
    config['sub_scene'] = buttons_scenes[0][1]
    test_group.leave_buttons()

    for test_button in test_group:
        if test_button.scene == config['scene'] and test_button.sub_scene == config['sub_scene']:
            assert test_button.action == 'leave'
        else:
            assert test_button.action == 'stop'

    # Test `leave_buttons` method with parameters
    test_buttons = create_buttons()
    test_group = SceneButtonsGroup(config, *test_buttons)
    scene = buttons_scenes[1][0]
    sub_scene = buttons_scenes[1][1]
    test_group.leave_buttons(scene, sub_scene)

    for test_button in test_group:
        if test_button.scene == scene and test_button.sub_scene == sub_scene:
            assert test_button.action == 'leave'
        else:
            assert test_button.action == 'stop'
