""" File with implementation of various utility functions """

from functools import lru_cache

import pygame


@lru_cache(maxsize=4)
def _circle_points(r):
    """Descretization of a circle into a list of points

    Args:
        r (int): Circle radius

    Returns:
        List[Tuple[int, int]]: List of points representing a circle with
            given radius
    """
    x, y, e = r, 0, 1 - r

    points = []

    while x >= y:
        points.append((x, y))

        y += 1
        if e < 0:
            e += 2 * y - 1
        else:
            x -= 1
            e += 2 * (y - x) - 1

    points += [(y, x) for x, y in points if x > y]
    points += [(-x, y) for x, y in points if x]
    points += [(x, -y) for x, y in points if y]

    return points


def render(font, text, color, border=0, bcolor=None):
    """Analog of the :method:`pygame.font.Font.render` with support of a
    border around the font

    Args:
        font (pygame.font.Font): Font object
        text (str): The text you need to render
        color (pygame.Color): Text color
        border (int): Border width
        bcolor (pygame.Color): Border color

    Returns:
        pygame.Surface: Rendered text
    """
    text_surface = font.render(text, True, color).convert_alpha()
    w = text_surface.get_width() + 2 * border
    h = font.get_height() + 2 * border

    osurf = pygame.Surface((w, h)).convert_alpha()
    osurf.fill((0, 0, 0, 0))

    surf = osurf.copy()

    osurf.blit(font.render(text, True, bcolor).convert_alpha(), (0, 0))

    for dx, dy in _circle_points(border):
        surf.blit(osurf, (dx + border, dy + border))

    surf.blit(text_surface, (border, border))

    return surf
