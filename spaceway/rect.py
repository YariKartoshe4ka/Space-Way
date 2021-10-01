""" File with extension of default `pygame.Rect` to use it with float values """

import pygame


class FloatRect:
    def __init__(self, *args):
        if len(args) == 2:
            if len(args[0]) == 2 and len(args[1]) == 2:
                l = [*args[0], *args[1]]
            else:
                raise TypeError("Argument must be rect style object")
        elif len(args) == 4:
            l = [*args]
        elif len(args) == 1:
            if len(args[0]) == 2:
                l = [*args[0][0], *args[0][1]]
            elif len(args[0]) == 4:
                l = list(args[0])
            else:
                raise TypeError(
                    f"sequence argument takes 2 or 4 items ({len(args[0])} given)"
                )

        else:
            raise TypeError("Argument must be rect style object")

        self.__dict__["_rect"] = l

    getattr_dict = {
        "x": lambda x: x._rect[0],
        "y": lambda x: x._rect[1],
        "top": lambda x: x._rect[1],
        "left": lambda x: x._rect[0],
        "bottom": lambda x: x._rect[1] + x._rect[3],
        "right": lambda x: x._rect[0] + x._rect[2],
        "topleft": lambda x: (x._rect[0], x._rect[1]),
        "bottomleft": lambda x: (x._rect[0], x._rect[1] + x._rect[3]),
        "topright": lambda x: (x._rect[0] + x._rect[2], x._rect[1]),
        "bottomright": lambda x: (x._rect[0] + x._rect[2], x._rect[1] + x._rect[3]),
        "midtop": lambda x: (x._rect[0] + x._rect[2] / 2, x._rect[1]),
        "midleft": lambda x: (x._rect[0], x._rect[1] + x._rect[3] / 2),
        "midbottom": lambda x: (x._rect[0] + x._rect[2] / 2, x._rect[1] + x._rect[3]),
        "midright": lambda x: (x._rect[0] + x._rect[2], x._rect[1] + x._rect[3] / 2),
        "center": lambda x: (x._rect[0] + x._rect[2] / 2, x._rect[1] + x._rect[3] / 2),
        "centerx": lambda x: x._rect[0] + x._rect[2] / 2,
        "centery": lambda x: x._rect[1] + x._rect[3] / 2,
        "size": lambda x: (x._rect[2], x._rect[3]),
        "width": lambda x: x._rect[2],
        "height": lambda x: x._rect[3],
        "w": lambda x: x._rect[2],
        "h": lambda x: x._rect[3],
    }

    def __getattr__(self, name):
        try:
            return self.__class__.getattr_dict[name](self)
        except KeyError:
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute 'name'"
            )

    def __setattr__(self, name, value):
        if name == "x":
            self._rect[0] = value
            return

        if name == "y":
            self._rect[1] = value
            return

        if name == "top":
            self._rect[1] = value
            return

        if name == "left":
            self._rect[0] = value
            return

        if name == "bottom":
            self._rect[1] += value - self.bottom
            return

        if name == "right":
            self._rect[0] += value - self.right
            return

        if name == "topleft":
            self._rect[0], self._rect[1] = value
            return

        if name == "bottomleft":
            self._rect[0], self.bottom = value
            return

        if name == "topright":
            self.right, self._rect[1] = value
            return

        if name == "bottomright":
            self.right, self.bottom = value
            return

        if name == "midtop":
            self.centerx, self._rect[1] = value
            return

        if name == "midleft":
            self._rect[0], self.centery = value
            return

        if name == "midbottom":
            self.centerx, self.bottom = value
            return

        if name == "midright":
            self.right, self.centery = value
            return

        if name == "center":
            self.centerx, self.centery = value
            return

        if name == "centerx":
            self._rect[0] += value - self.centerx
            return

        if name == "centery":
            self._rect[1] += value - self.centery
            return

        if name == "size":
            self._rect[2], self._rect[3] = value
            return

        if name == "width":
            self._rect[2] = value
            return

        if name == "height":
            self._rect[3] = value
            return

        if name == "w":
            self._rect[2] = value
            return

        if name == "h":
            self._rect[3] = value
            return

        self.__dict__[name] = value

    def __getitem__(self, index):
        return self._rect[index]

    def __setitem__(self, index, value):
        self._rect[index] = value

    def __len__(self):
        return 4

    def __str__(self):
        return f"<pgx_rect{tuple(self._rect)}>"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        try:
            return self._rect == self.__class__(other)._rect
        except:
            return False

    def __bool__(self):
        return self._rect[2] != 0 and self._rect[3] != 0

    def copy(self):
        return self.__class__(self._rect)

    def move(self, x, y):
        c = self.copy()
        c.move_ip(x, y)
        return c

    def move_ip(self, x, y):
        self._rect[0] += x
        self._rect[1] += y

    def inflate(self, x, y):
        c = self.copy()
        c.inflate_ip(x, y)
        return c

    def inflate_ip(self, x, y):
        self._rect[0] -= x / 2
        self._rect[2] += x

        self._rect[1] -= y / 2
        self._rect[3] += y

    def update(self, *args):
        self.__init__(*args)

    def clamp(self, argrect):
        c = self.copy()
        c.clamp_ip(argrect)
        return c

    def clamp_ip(self, argrect):
        try:
            argrect = self.__class__(argrect)
        except:
            raise TypeError("Argument must be rect style object")

        if self._rect[2] >= argrect.w:
            x = argrect.x + argrect.w / 2 - self._rect[2] / 2
        elif self._rect[0] < argrect.x:
            x = argrect.x
        elif self._rect[0] + self._rect[2] > argrect.x + argrect.w:
            x = argrect.x + argrect.w - self._rect[2]
        else:
            x = self._rect[0]

        if self._rect[3] >= argrect.h:
            y = argrect.y + argrect.h / 2 - self._rect[3] / 2
        elif self._rect[1] < argrect.y:
            y = argrect.y
        elif self._rect[1] + self._rect[3] > argrect.y + argrect.h:
            y = argrect.y + argrect.h - self._rect[3]
        else:
            y = self._rect[1]

        self._rect[0] = x
        self._rect[1] = y

    def clip(self, argrect):
        try:
            argrect = self.__class__(argrect)
        except:
            raise TypeError("Argument must be rect style object")

        # left
        if self.x >= argrect.x and self.x < argrect.x + argrect.w:
            x = self.x
        elif argrect.x >= self.x and argrect.x < self.x + self.w:
            x = argrect.x
        else:
            return self.__class__(self.x, self.y, 0, 0)

        # right
        if self.x + self.w > argrect.x and self.x + self.w <= argrect.x + argrect.w:
            w = self.x + self.w - x
        elif (
            argrect.x + argrect.w > self.x and argrect.x + argrect.w <= self.x + self.w
        ):
            w = argrect.x + argrect.w - x
        else:
            return self.__class__(self.x, self.y, 0, 0)

        # top
        if self.y >= argrect.y and self.y < argrect.y + argrect.h:
            y = self.y
        elif argrect.y >= self.y and argrect.y < self.y + self.h:
            y = argrect.y
        else:
            return self.__class__(self.x, self.y, 0, 0)

        # bottom
        if self.y + self.h > argrect.y and self.y + self.h <= argrect.y + argrect.h:
            h = self.y + self.h - y
        elif (
            argrect.y + argrect.h > self.y and argrect.y + argrect.h <= self.y + self.h
        ):
            h = argrect.y + argrect.h - y
        else:
            return self.__class__(self.x, self.y, 0, 0)

        return self.__class__(x, y, w, h)

    def union(self, argrect):
        c = self.copy()
        c.union_ip(argrect)
        return c

    def union_ip(self, argrect):
        try:
            argrect = self.__class__(argrect)
        except:
            raise TypeError("Argument must be rect style object")

        x = min(self.x, argrect.x)
        y = min(self.y, argrect.y)
        w = max(self.x + self.w, argrect.x + argrect.w) - x
        h = max(self.y + self.h, argrect.y + argrect.h) - y

        self._rect = [x, y, w, h]

    def unionall(self, argrects):
        c = self.copy()
        c.unionall_ip(argrects)
        return c

    def unionall_ip(self, argrects):
        for i, argrect in enumerate(argrects):
            try:
                argrects[i] = self.__class__(argrect)
            except:
                raise TypeError("Argument must be rect style object")

        x = min([self.x] + [r.x for r in argrects])
        y = min([self.y] + [r.y for r in argrects])
        w = max([self.right] + [r.right for r in argrects]) - x
        h = max([self.bottom] + [r.bottom for r in argrects]) - y

        self._rect = [x, y, w, h]

    def fit(self, argrect):
        try:
            argrect = self.__class__(argrect)
        except:
            raise TypeError("Argument must be rect style object")

        xratio = self.w / argrect.w
        yratio = self.h / argrect.h
        maxratio = max(xratio, yratio)

        w = self.w / maxratio
        h = self.h / maxratio

        x = argrect.x + (argrect.w - w) / 2
        y = argrect.y + (argrect.h - h) / 2

        return self.__class__(x, y, w, h)

    def normalize(self):
        if self._rect[2] < 0:
            self._rect[0] += self._rect[2]
            self._rect[2] = -self._rect[2]

        if self._rect[3] < 0:
            self._rect[1] += self._rect[3]
            self._rect[3] = -self._rect[3]

    def contains(self, argrect):
        try:
            argrect = self.__class__(argrect)
        except:
            raise TypeError("Argument must be rect style object")

        if self._rect[0] <= argrect[0] and argrect[0] + argrect[2] <= self.right:
            if self._rect[1] <= argrect[1] and argrect[1] + argrect[3] <= self.bottom:
                return True
        return False

    def collidepoint(self, *args):
        if len(args) == 1:
            point = args[0]
        elif len(args) == 2:
            point = tuple(args)
        else:
            raise TypeError("argument must contain two numbers")

        # conforms with no collision on right / bottom edge behavior of pygame FloatRects
        if self._rect[0] <= point[0] < self.right:
            if self._rect[1] <= point[1] < self.bottom:
                return True
        return False

    def colliderect(self, argrect):
        try:
            argrect = self.__class__(argrect)
        except:
            raise TypeError("Argument must be rect style object")

        if any(0 == d for d in [self.w, self.h, argrect.w, argrect.h]):
            return False

        return (
            min(self.x, self.x + self.w) < max(argrect.x, argrect.x + argrect.w)
            and min(self.y, self.y + self.h) < max(argrect.y, argrect.y + argrect.h)
            and max(self.x, self.x + self.w) > min(argrect.x, argrect.x + argrect.w)
            and max(self.y, self.y + self.h) > min(argrect.y, argrect.y + argrect.h)
        )

    def collidelist(self, argrects):
        for i, argrect in enumerate(argrects):
            if self.colliderect(argrect):
                return i

        return -1

    def collidelistall(self, argrects):
        out = []

        for i, argrect in enumerate(argrects):
            if self.colliderect(argrect):
                out.append(i)

        return out

    def collidedict(self, rects_dict, use_values=0):
        for key in rects_dict:
            if use_values == 0:
                argrect = key
            else:
                argrect = rects_dict[key]

            if self.colliderect(argrect):
                return (key, rects_dict[key])

        return None  # explicit rather than implicit

    def collidedictall(self, rects_dict, use_values=0):
        out = []

        for key in rects_dict:
            if use_values == 0:
                argrect = key
            else:
                argrect = rects_dict[key]

            if self.colliderect(argrect):
                out.append((key, rects_dict[key]))

        return out
