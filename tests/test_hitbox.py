from random import randint
from re import match

import pytest
from pygame import Rect as PgRect

from spaceway.hitbox import Hitbox, Rect, Ellipse
from utils import rstring


def test_hitbox_init():
    assert (
        Hitbox(100, 123, 10, 29) == Hitbox((100, 123), (10, 29)) ==
        Hitbox((100, 123, 10, 29)) == Hitbox(((100, 123), (10, 29))) ==
        Hitbox(Hitbox(100, 123, 10, 29)) == Hitbox(Rect(100, 123, 10, 29)) ==
        Hitbox(Ellipse(100, 123, 10, 29)) == Hitbox(PgRect(100, 123, 10, 29)) ==
        PgRect(Hitbox(100, 123, 10, 29))
    )
    assert (
        Hitbox(-100, 2, 0, -2) == Hitbox((-100, 2), (0, -2)) ==
        Hitbox((-100, 2, 0, -2)) == Hitbox(((-100, 2), (0, -2))) ==
        Hitbox(Hitbox(-100, 2, 0, -2)) == Hitbox(Rect(-100, 2, 0, -2)) ==
        Hitbox(Ellipse(-100, 2, 0, -2)) == Hitbox(PgRect(-100, 2, 0, -2)) ==
        PgRect(Hitbox(-100, 2, 0, -2))
    )

    with pytest.raises(TypeError, match='Argument must be hitbox style object'):
        Hitbox((100, 123), (10,))

    with pytest.raises(TypeError, match='Argument must be hitbox style object'):
        Hitbox((100,), (10,))

    with pytest.raises(TypeError, match=r'sequence argument takes 2 or 4 items \(\d given\)'):
        Hitbox((100, 123, 10))

    with pytest.raises(TypeError, match='Argument must be hitbox style object'):
        Hitbox(100, 123, 10)


def test_rect_init():
    assert (
        Rect(100, 123, 10, 29) == Rect((100, 123), (10, 29)) ==
        Rect((100, 123, 10, 29)) == Rect(((100, 123), (10, 29))) ==
        Rect(Hitbox(100, 123, 10, 29)) == Rect(Rect(100, 123, 10, 29)) ==
        Rect(Ellipse(100, 123, 10, 29)) == Rect(PgRect(100, 123, 10, 29)) ==
        PgRect(Rect(100, 123, 10, 29))
    )
    assert (
        Rect(-100, 2, 0, -2) == Rect((-100, 2), (0, -2)) ==
        Rect((-100, 2, 0, -2)) == Rect(((-100, 2), (0, -2))) ==
        Rect(Hitbox(-100, 2, 0, -2)) == Rect(Rect(-100, 2, 0, -2)) ==
        Rect(Ellipse(-100, 2, 0, -2)) == Rect(PgRect(-100, 2, 0, -2)) ==
        PgRect(Rect(-100, 2, 0, -2))
    )

    with pytest.raises(TypeError, match='Argument must be hitbox style object'):
        Rect((100, 123), (10,))

    with pytest.raises(TypeError, match='Argument must be hitbox style object'):
        Rect((100,), (10,))

    with pytest.raises(TypeError, match=r'sequence argument takes 2 or 4 items \(\d given\)'):
        Rect((100, 123, 10))

    with pytest.raises(TypeError, match='Argument must be hitbox style object'):
        Rect(100, 123, 10)


def test_ellipse_init():
    assert (
        Ellipse(100, 123, 10, 29) == Ellipse((100, 123), (10, 29)) ==
        Ellipse((100, 123, 10, 29)) == Ellipse(((100, 123), (10, 29))) ==
        Ellipse(Hitbox(100, 123, 10, 29)) == Ellipse(Rect(100, 123, 10, 29)) ==
        Ellipse(Ellipse(100, 123, 10, 29)) == Ellipse(PgRect(100, 123, 10, 29)) ==
        PgRect(Ellipse(100, 123, 10, 29))
    )
    assert (
        Ellipse(-100, 2, 0, -2) == Ellipse((-100, 2), (0, -2)) ==
        Ellipse((-100, 2, 0, -2)) == Ellipse(((-100, 2), (0, -2))) ==
        Ellipse(Hitbox(-100, 2, 0, -2)) == Ellipse(Rect(-100, 2, 0, -2)) ==
        Ellipse(Ellipse(-100, 2, 0, -2)) == Ellipse(PgRect(-100, 2, 0, -2)) ==
        PgRect(Ellipse(-100, 2, 0, -2))
    )

    with pytest.raises(TypeError, match='Argument must be hitbox style object'):
        Ellipse((100, 123), (10,))

    with pytest.raises(TypeError, match='Argument must be hitbox style object'):
        Ellipse((100,), (10,))

    with pytest.raises(TypeError, match=r'sequence argument takes 2 or 4 items \(\d given\)'):
        Ellipse((100, 123, 10))

    with pytest.raises(TypeError, match='Argument must be hitbox style object'):
        Ellipse(100, 123, 10)


@pytest.mark.parametrize('hitbox', [
    Hitbox(100, 123, 10, 29),
    Hitbox(-100, 2, 0, -2),
    Hitbox(41, -32, -25, -1),
    Rect(100, 123, 10, 29),
    Rect(-100, 2, 0, -2),
    Rect(41, -32, -25, -1),
    Ellipse(100, 123, 10, 29),
    Ellipse(-100, 2, 0, -2),
    Ellipse(41, -32, -25, -1),
])
def test_generic(hitbox):
    # Test `copy` method
    assert hitbox.copy() == hitbox

    # Test magic methods
    hitbox_copy = hitbox.copy()

    hitbox_copy[0], hitbox_copy[1], hitbox_copy[2], hitbox_copy[3] = range(4)
    assert (
        hitbox_copy[0] == 0 and hitbox_copy[1] == 1 and
        hitbox_copy[2] == 2 and hitbox_copy[3] == 3
    )
    assert len(hitbox) == len(PgRect(hitbox))
    assert bool(hitbox) == bool(PgRect(hitbox))
    assert not (hitbox == rstring())

    p = r'^<\w+\(((-?\d+|-?\d+\.\d+), ){3}(-?\d+|-?\d+\.\d+)\)>$'
    assert match(p, str(hitbox)) and match(p, repr(hitbox))

    assert hash(hitbox) == hash(str(hitbox))

    # Test `getattr_dict` and methods which operates with it
    hitbox_copy = hitbox.copy()

    for attr in hitbox_copy.getattr_dict.keys():
        a = getattr(hitbox_copy, attr)

        if isinstance(a, int) or isinstance(a, float):
            v1 = randint(-1000, 1000)
            v2 = 0
        else:
            v1 = (randint(-1000, 1000), randint(-1000, 1000))
            v2 = (0, 0)

        # Log attribute name on fail
        print(f'attr={attr} v1={v1} v2={v2}' + ' ' * 15, end='\r')

        setattr(hitbox_copy, attr, v1)
        assert getattr(hitbox_copy, attr) == v1

        setattr(hitbox_copy, attr, v2)
        assert getattr(hitbox_copy, attr) == v2

    # Test other methods
    x, y = (10, -10)

    # Test `trunc` (`trunc_ip`)
    hitbox_copy = hitbox.copy()
    for i in range(len(hitbox_copy._rect)):
        hitbox_copy._rect[i] += 1e-04

    assert hitbox_copy.trunc() == PgRect(hitbox_copy)

    # Test `move` (`move_ip`) and `inflate` (`inflate_ip`)
    assert hitbox.move(x, y).trunc() == PgRect(hitbox).move(x, y)
    assert hitbox.inflate(x, y).trunc() == PgRect(hitbox).inflate(x, y)

    # Test `normalize`
    hitbox_copy = hitbox.copy()
    pgrect = PgRect(hitbox_copy)
    hitbox_copy.normalize()
    pgrect.normalize()

    assert hitbox_copy.trunc() == pgrect

    # Test `update`
    hitbox_copy.update(hitbox)
    assert hitbox_copy == hitbox


@pytest.mark.parametrize('arg,exception', [
    (Ellipse(150, 70, 73, 130), NotImplementedError),
    (Ellipse(198, 190, 65, 20), NotImplementedError),
    (Rect(100, 123, 10, 29), NotImplementedError),
    (Rect(-100, 2, 40, -2), NotImplementedError),
    (154, TypeError),
    ('qwertyasd', TypeError)
])
def test_exceptions(arg, exception):
    hitbox = Hitbox(100, 123, 10, 29)

    methods_with_arg = ('clamp', 'clip', 'union', 'fit', 'contains', 'colliderect')
    methods_with_args = ('unionall', 'collidelist', 'collidelistall')

    for method in methods_with_arg:
        with pytest.raises(exception):
            getattr(hitbox, method)(arg)

    for method in methods_with_args:
        with pytest.raises(exception):
            getattr(hitbox, method)([arg])

    with pytest.raises(TypeError):
        hitbox.collidepoint(1, 2, 3)

    with pytest.raises(NotImplementedError):
        hitbox.collidepoint(1, 2)


@pytest.mark.parametrize('rect', [
    Rect(23, 83, 40, 10),
    Rect(100, 83, 120, 251),
])
@pytest.mark.parametrize('arg', [
    Rect(100, 123, 10, 29),
    Rect(-100, 2, 0, -2),
    PgRect(100, 123, 10, 29),
    PgRect(-100, 2, 0, -2)
])
def test_rect_with_rect(rect, arg):
    # Test `clamp (_ip)`, `clip`, `union (_ip)`, `fit`, `contains` and `colliderect`
    assert rect.clamp(arg).trunc() == PgRect(rect).clamp(arg)
    assert rect.clip(arg).trunc() == PgRect(rect).clip(arg)
    assert rect.union(arg).trunc() == PgRect(rect).union(arg)
    assert rect.fit(arg).trunc() == PgRect(rect).fit(arg)
    assert rect.contains(arg) == PgRect(rect).contains(arg)
    assert rect.colliderect(arg) == PgRect(rect).colliderect(arg)

    # Test `unionall (_ip)`, `collidelist` and `collidelistall`
    assert rect.unionall([arg, rect]) == PgRect(rect).unionall([arg, rect])
    assert rect.collidelist([arg, rect, arg, rect]) == PgRect(rect).collidelist([arg, rect, arg, rect])
    assert rect.collidelist([]) == PgRect(rect).collidelist([])
    assert rect.collidelistall([arg, rect, arg, rect]) == PgRect(rect).collidelistall([arg, rect, arg, rect])
    assert rect.collidelistall([]) == PgRect(rect).collidelistall([])

    # Test `collidedict` and `collidedictall`
    assert (
        rect.collidedict({0: arg, 1: rect, True: arg, None: rect}, True) ==
        PgRect(rect).collidedict({0: arg, 1: rect, True: arg, None: rect}, True)
    )
    assert rect.collidedict({rect: 0}) == PgRect(rect).collidedict({rect: 0})
    assert rect.collidedict({}) == PgRect(rect).collidedict({})

    assert (
        rect.collidedictall({0: arg, 1: rect, True: arg, None: rect}, True) ==
        PgRect(rect).collidedictall({0: arg, 1: rect, True: arg, None: rect}, True)
    )
    assert rect.collidedictall({rect: 0}) == PgRect(rect).collidedictall({rect: 0})
    assert rect.collidedictall({}) == PgRect(rect).collidedictall({})

    # Test `collidepoint`
    point1 = (randint(-20, 20), randint(-20, 20))
    point2 = (0, 0)

    assert rect.collidepoint(point1) == PgRect(rect).collidepoint(point1)
    assert rect.collidepoint(*point1) == PgRect(rect).collidepoint(*point1)

    assert rect.collidepoint(point2) == PgRect(rect).collidepoint(point2)
    assert rect.collidepoint(*point2) == PgRect(rect).collidepoint(*point2)


@pytest.mark.parametrize('rect,arg,expected', [
    (Rect(10, 50, 83, 127), Ellipse(68, 59, 90, 72), (False, True)),
    (Rect(140, 152, 103, 73), Ellipse(61, 76, 90, 81), (False, False)),
    (Rect(-30, -16, 88, 73), Ellipse(53, 30, 90, 81), (False, True)),
    (Rect(71, 24, 190, 69), Ellipse(83, -65, 140, 92), (False, True)),
    (Rect(71, 213, 180, 140), Ellipse(102, 226, 140, 125), (True, True))
])
def test_rect_with_ellipse(rect, arg, expected):
    assert rect.contains(arg) == expected[0]
    assert rect.colliderect(arg) == expected[1]


@pytest.mark.parametrize('ellipse,expected', [
    (Ellipse(150, 70, 73, 130), (False,)),
    (Ellipse(198, 190, 65, 20), (True,)),
    (Ellipse(196, 188, 58, 131), (False,)),
    (Ellipse(150, 160, 97, 90), (True,))
])
def test_ellipse(ellipse, expected):
    point = (200, 200)
    assert ellipse.collidepoint(point) == expected[0]
    assert ellipse.collidepoint(*point) == expected[0]


@pytest.mark.parametrize('ellipse,arg,expected', [
    (Ellipse(20, 30, 41, 70), Rect(55, 51, 61, 40), (False, True)),
    (Ellipse(30, 50, 80, 42), Rect(-5, -10, 40, 68), (False, False)),
    (Ellipse(40, 80, 70, 59), Rect(98, 57, 70, 40), (False, True)),
    (Ellipse(-70, 39, 42, 80), Rect(-30, 39, 42, 80), (False, True)),
    (Ellipse(71, 42, 73, 130), Rect(99, 52, 10, 5), (True, True)),
    (Ellipse(20, 30, 41, 70), PgRect(55, 51, 61, 40), (False, True)),
    (Ellipse(30, 50, 80, 42), PgRect(-5, -10, 40, 68), (False, False)),
    (Ellipse(40, 80, 70, 59), PgRect(98, 57, 70, 40), (False, True)),
    (Ellipse(-70, 39, 42, 80), PgRect(-30, 39, 42, 80), (False, True)),
    (Ellipse(71, 42, 73, 130), PgRect(99, 52, 10, 5), (True, True))
])
def test_ellipse_with_rect(ellipse, arg, expected):
    assert ellipse.contains(arg) == expected[0]
    assert ellipse.colliderect(arg) == expected[1]


@pytest.mark.parametrize('ellipse,arg,expected', [
    (Ellipse(17, 28, 124, 90), Ellipse(42, 10, 91, 130), (False, True)),
    (Ellipse(51, 10, 38, 70), Ellipse(85, 65, 120, 39), (False, False)),
    (Ellipse(104, 201, 120, 180), Ellipse(50, 176, 84, 39), (False, False)),
    (Ellipse(20, 87, 111, 98), Ellipse(86, 100, 36, 45), (True, True)),
    (Ellipse(-40, 32, 85, 24), Ellipse(44, 17, 30, 54), (False, True)),
    (Ellipse(58, 74, 198, 166), Ellipse(76, 91, 54, 50), (False, True)),
    (Ellipse(-100, -100, 115, 84), Ellipse(-100, -100, 115, 84), (True, True)),
    # (Ellipse(34, 80, 10, 100), Ellipse(34, 82, 100, 10), (False, True)) - Problem test
])
def test_ellipse_with_ellipse(ellipse, arg, expected):
    assert ellipse.contains(arg) == expected[0]
    assert ellipse.colliderect(arg) == expected[1]
