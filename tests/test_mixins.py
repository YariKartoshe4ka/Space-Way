from random import randint
from math import inf
from time import time

import pytest
import pygame

from spaceway.mixins import *
from spaceway.hitbox import Ellipse
from spaceway.collection import SceneButtonsGroup
from utils import *


@pytest.mark.parametrize('params,expected', [
    [(46, 88, -4, -29, 30), (30, 30)],
    [(121, 290, 20, -30, 290), (-30, 290)],
    [(-15, 93, -6, 30, 93), (93, 30)],
    [(20, -40, 15, -40, 151), (-40, 151)],
    [(32, -48, -5, -48, 86), (86, -48)],
    [(85, 10, -8, 10, 90), (90, 10)],
    [(-14, -4, -5, -4, 32), (32, -4)],
    [(-8, 32, 6, -52, 32), (-52, 32)],
    [(30, 56, 7, 5, 60), (5, 60)],
    [(-51, -11, -7, -35, 24), (24, -35)],
    [(13, 118, 0, -inf, inf), (118, 118)]
])
def test_scene_button_mixin_actions(pygame_env, params, expected):
    screen, base_dir, config, clock = pygame_env
    x, y, speed, top, bottom = params

    class TestSceneButton(SceneButtonMixin):
        def __init__(self, action='stop'):
            self.screen = screen
            self.img = pygame_surface((randint(20, 120), randint(20, 120)))
            self.rect = Ellipse(self.img.get_rect())
            self.rect.topleft = (x, y)
            SceneButtonMixin.__init__(
                self, base_dir, config, '', '', '', '',
                speed, top, bottom, action
            )

        def draw(self):
            self.update()
            self.blit()

    # Test stop action which passed in `__init__` function
    test_button = TestSceneButton()

    @pygame_loop(pygame_env, 0.5)
    def loop1():
        test_button.draw()

    assert test_button.rect.topleft == (x, y)

    # Test enter action which passed in `__init__` function
    test_button = TestSceneButton('enter')

    @pygame_loop(pygame_env, 1)
    def loop2():
        test_button.draw()

    assert test_button.rect.topleft == (x, expected[0])

    # Test leave action which passed in `__init__` function
    test_button = TestSceneButton('leave')

    @pygame_loop(pygame_env, 1)
    def loop3():
        test_button.draw()

    assert test_button.rect.topleft == (x, expected[1])

    # Test enter action which activated via method
    test_button = TestSceneButton()
    test_button.enter()

    @pygame_loop(pygame_env, 1)
    def loop4():
        test_button.draw()

    assert test_button.rect.topleft == (x, expected[0])

    # Test leave action which activated via method
    test_button = TestSceneButton()
    test_button.leave()

    @pygame_loop(pygame_env, 1)
    def loop5():
        test_button.draw()

    assert test_button.rect.topleft == (x, expected[1])


@pytest.mark.parametrize('params,expected', [
    [(120, 90, -9, 20, 90), 20],
    [(-10, 23, 4, 10, 60), 60],
    [(30, 42, 0, 42, 42), 42]
])
def test_scene_button_mixin_scenes(pygame_env, params, expected):
    screen, base_dir, config, clock = pygame_env
    x, y, speed, top, bottom = params

    scene, sub_scene, change_scene_to, change_sub_scene_to \
        = [rstring() for _ in range(4)]

    class TestSceneButton(SceneButtonMixin):
        def __init__(self, pos=(x, y), speed=speed, top=top, bottom=bottom, scene=scene,
                     sub_scene=sub_scene, change_scene_to=change_scene_to,
                     change_sub_scene_to=change_sub_scene_to):
            self.screen = screen
            self.img = pygame_surface((randint(20, 120), randint(20, 120)))
            self.rect = Ellipse(self.img.get_rect())
            self.rect.topleft = pos
            SceneButtonMixin.__init__(
                self, base_dir, config, scene, sub_scene, change_scene_to,
                change_sub_scene_to, speed, top, bottom
            )

        def draw(self):
            self.update()
            self.blit()

    # Test `change_scene` method
    test_button = TestSceneButton()
    test_button.change_scene()

    assert config['scene'] == change_scene_to and config['sub_scene'] == change_sub_scene_to

    # Test `press` method
    config['scene'] = scene
    config['sub_scene'] = sub_scene

    test_button = TestSceneButton()
    test_button1 = TestSceneButton((0, 0), -5, 0, 50, change_scene_to, change_sub_scene_to)

    _ = SceneButtonsGroup(config, test_button, test_button1)
    test_button.press()

    @pygame_loop(pygame_env, 2)
    def loop():
        if config['scene'] == change_scene_to and config['sub_scene'] == change_sub_scene_to:
            test_button1.draw()
        else:
            test_button.draw()

    assert config['scene'] == change_scene_to and config['sub_scene'] == change_sub_scene_to
    assert test_button.rect.top == expected
    assert test_button1.rect.top == 50


@pytest.mark.parametrize('params', [
    ('abcdefzxcv', (510, 54)),
    ('asdasdafhreh', (123, 321)),
    ('qwertyuiodfer', (11, 223)),
    ('apodmebzx', (34, 89)),
    ('poiuyaaffee', (0, -10))
])
def test_caption_mixin(pygame_env, params):
    screen, base_dir, config, clock = pygame_env
    caption, topleft = params

    class TestCaption(CaptionMixin):
        def __init__(self):
            self.screen = screen
            CaptionMixin.__init__(self, base_dir, config, caption)

        def draw(self):
            self.update()
            self.blit()

    # Test first color
    config['user']['color'] = 0
    test_caption = TestCaption()

    @pygame_loop(pygame_env, 0.5)
    def loop1():
        test_caption.draw()
        assert test_caption.rect.topleft == (0, 0)

    colors = most_popular_colors(screen, 2, [(0, 0, 0)])
    assert colors == [(255, 255, 255), (0, 153, 255)]

    # Test second color
    config['user']['color'] = 1
    test_caption = TestCaption()

    @pygame_loop(pygame_env, 0.5)
    def loop2():
        test_caption.draw()
        assert test_caption.rect.topleft == (0, 0)

    colors = most_popular_colors(screen, 2, [(0, 0, 0)])
    assert colors == [(255, 255, 255), (252, 15, 192)]

    # Test third color
    config['user']['color'] = 2
    test_caption = TestCaption()

    @pygame_loop(pygame_env, 0.5)
    def loop3():
        test_caption.draw()
        assert test_caption.rect.topleft == (0, 0)

    colors = most_popular_colors(screen, 2, [(0, 0, 0)])
    assert colors == [(255, 255, 255), (0, 255, 0)]

    # Test `locate` method
    def locate(self):
        self.rect.topleft = topleft

    TestCaption.locate = locate
    test_caption = TestCaption()

    @pygame_loop(pygame_env, 0.5)
    def loop4():
        assert test_caption.rect.topleft == topleft
        test_caption.draw()


@pytest.mark.parametrize('params,expected', [
    [(False, {True: pygame_surface((63, 63)), False: pygame_surface((63, 63), 1)}, None),
     (True, False)],
    [(True, {True: pygame_surface((42, 20)), False: pygame_surface((42, 20), 1)}, None),
     (False, True)],
    [(
        0, {0: pygame_surface((58, 32)), 1: pygame_surface((58, 32), 1), 2: pygame_surface((58, 32), 2)},
        lambda self: setattr(self, 'state', (self.state + 1) % 3)
    ), (1, 2, 0)],
    [(
        'a', {'a': pygame_surface((41, 71)), 'aa': pygame_surface((41, 71), 1), 'aaa': pygame_surface((41, 71), 2)},
        lambda self: setattr(self, 'state', 'a' if len(self.state) == 3 else self.state + 'a')
    ), ('aa', 'aaa', 'a')],
    [(
        2, {0: pygame_surface((60, 55)), 1: pygame_surface((60, 55), 1),
            2: pygame_surface((60, 55), 2), 3: pygame_surface((60, 55), 1)},
        lambda self: setattr(self, 'state', (self.state - 1) % 4)
    ), (1, 0, 3, 2)]
])
def test_setttings_button_mixin(pygame_env, params, expected):
    screen, base_dir, config, clock = pygame_env
    config_value, imgs, change_state = params
    config_index = rstring(15)

    class TestSettingsButton(SettingsButtonMixin):
        def __init__(self):
            self.imgs = imgs
            SettingsButtonMixin.__init__(self, screen, config, config_index)

        def draw(self):
            self.update()
            self.blit()

    # Test `update` and `blit` methods
    config['user'][config_index] = config_value

    test_button = TestSettingsButton()
    assert test_button.state == config_value
    assert test_button.img == test_button.imgs[config_value]

    @pygame_loop(pygame_env, 0.5)
    def loop1():
        test_button.draw()

    # Test `change_state` with `update` method
    if change_state:
        TestSettingsButton.change_state = change_state

    test_button = TestSettingsButton()

    for state in expected:
        test_button.change_state()
        assert test_button.state == state

        test_button.update()
        assert test_button.img == test_button.imgs[state]

    # Test `press` with method
    test_button = TestSettingsButton()

    for state in expected:
        test_button.press()
        assert test_button.state == state
        assert test_button.img == test_button.imgs[state]


@pytest.mark.parametrize('life', [
    4, 2, 6
])
def test_boost_mixin(pygame_env, life):
    screen, base_dir, config, clock = pygame_env

    class TestBoost(BoostMixin):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)

            self.img_idle = pygame_surface((30, 30))
            self.img_small = pygame_surface((18, 18), 1)
            self.number_in_queue = randint(1, 4)

            BoostMixin.__init__(self, screen, base_dir, config, rstring(), life)

        def draw(self):
            self.update()
            self.blit()

    config['ns'].speed = 18

    # Test boost alive and position
    test_boost = TestBoost()
    y = test_boost.rect.y

    assert test_boost.rect.x == screen.get_width()
    assert 0 <= y <= screen.get_height() - test_boost.rect.h - 2
    assert test_boost.rect_small.topleft == (2, 0)

    _ = pygame.sprite.Group(test_boost)

    @pygame_loop(pygame_env, 2)
    def loop1():
        test_boost.draw()

    assert test_boost.rect.right < 0
    assert test_boost.rect.y == y
    assert not test_boost.alive()

    # Test boost life time after activation
    test_boost = TestBoost()
    test_boost.activate()

    _ = pygame.sprite.Group(test_boost)
    assert test_boost.alive()

    @pygame_loop(pygame_env, life)
    def loop2():
        test_boost.draw()

    assert not test_boost.alive()

    # Test boost color of life time
    test_boost = TestBoost()
    test_boost.activate()
    test_boost.update()
    assert (
        most_popular_colors(test_boost.img_life, 1, [(0, 0, 0)])[0] ==
        (BoostMixin.COLOR_LONG if life > 2 else BoostMixin.COLOR_SHORT)
    )

    @pygame_loop(pygame_env, life - 2.9)
    def loop3():
        test_boost.draw()

    assert most_popular_colors(test_boost.img_life, 1, [(0, 0, 0)])[0] == BoostMixin.COLOR_SHORT

    # Test custom `deactivate` method
    TestBoost.deactivate = lambda self: 1 / 0

    test_boost = TestBoost()
    test_boost.activate()

    with pytest.raises(ZeroDivisionError):
        @pygame_loop(pygame_env, life + 1)
        def loop4():
            test_boost.draw()
