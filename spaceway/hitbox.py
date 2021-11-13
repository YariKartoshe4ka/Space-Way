""" File with implementation of hitboxes for calculating collisions,
    position and other. Based on `pygame.Rect` """

from math import sqrt, atan2, pi, sin, cos


class Hitbox:
    def __init__(self, *args):
        if len(args) == 2:
            if len(args[0]) == 2 and len(args[1]) == 2:
                l = [*args[0], *args[1]]
            else:
                raise TypeError("Argument must be hitbox style object")
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
            raise TypeError("Argument must be hitbox style object")

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
                f"'{self.__class__.__name__}' object has no attribute '{name}'"
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
        return f"<hitbox{tuple(self._rect)}>"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        try:
            return self._rect == self.__class__(other)._rect
        except:
            return False

    def __bool__(self):
        return self._rect[2] != 0 and self._rect[3] != 0

    def __hash__(self):
        return hash(str(self))

    def copy(self):
        return self.__class__(self._rect)

    def trunc(self):
        c = self.copy()
        c.trunc_ip()
        return c

    def trunc_ip(self):
        for i in range(len(self._rect)):
            self._rect[i] = int(self._rect[i])

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

    def clamp(self, arg):
        c = self.copy()
        c.clamp_ip(arg)
        return c

    def clamp_ip(self, arg):
        try:
            self.__class__(arg)
        except:
            raise TypeError("Argument must be hitbox style object")

        if isinstance(arg, Ellipse):
            return self._clamp_ip_ellipse(Ellipse(arg))
        return self._clamp_ip_rect(Rect(arg))

    def _clamp_ip_rect(self, rect):
        raise NotImplementedError('Method hasn\'t been implemented yet')

    def _clamp_ip_ellipse(self, ellipse):
        raise NotImplementedError('Method hasn\'t been implemented yet')

    def clip(self, arg):
        try:
            self.__class__(arg)
        except:
            raise TypeError("Argument must be hitbox style object")

        if isinstance(arg, Ellipse):
            return self._clip_ellipse(Ellipse(arg))
        return self._clip_rect(Rect(arg))

    def _clip_rect(self, rect):
        raise NotImplementedError('Method hasn\'t been implemented yet')

    def _clip_ellipse(self, ellipse):
        raise NotImplementedError('Method hasn\'t been implemented yet')

    def union(self, arg):
        c = self.copy()
        c.union_ip(arg)
        return c

    def union_ip(self, arg):
        try:
            self.__class__(arg)
        except:
            raise TypeError("Argument must be hitbox style object")

        if isinstance(arg, Ellipse):
            return self._union_ip_ellipse(Ellipse(arg))
        return self._union_ip_rect(arg)

    def _union_ip_rect(self, rect):
        raise NotImplementedError('Method hasn\'t been implemented yet')

    def _union_ip_ellipse(self, ellipse):
        raise NotImplementedError('Method hasn\'t been implemented yet')

    def unionall(self, args):
        c = self.copy()
        c.unionall_ip(args)
        return c

    def unionall_ip(self, args):
        for arg in args:
            try:
                self.__class__(arg)
            except:
                raise TypeError("Argument must be hitbox style object")

            self.union_ip(arg)

    def fit(self, arg):
        try:
            self.__class__(arg)
        except:
            raise TypeError("Argument must be hitbox style object")

        if isinstance(arg, Ellipse):
            return self._fit_ellipse(Ellipse(arg))
        return self._fit_rect(Rect(arg))

    def _fit_rect(self, rect):
        raise NotImplementedError('Method hasn\'t been implemented yet')

    def _fit_ellipse(self, ellipse):
        raise NotImplementedError('Method hasn\'t been implemented yet')

    def normalize(self):
        if self._rect[2] < 0:
            self._rect[0] += self._rect[2]
            self._rect[2] = -self._rect[2]

        if self._rect[3] < 0:
            self._rect[1] += self._rect[3]
            self._rect[3] = -self._rect[3]

    def contains(self, arg):
        try:
            self.__class__(arg)
        except:
            raise TypeError("Argument must be hitbox style object")

        if isinstance(arg, Ellipse):
            return self._contains_ellipse(Ellipse(arg))
        return self._contains_rect(Rect(arg))

    def _contains_rect(self, rect):
        raise NotImplementedError('Method hasn\'t been implemented yet')

    def _contains_ellipse(self, ellipse):
        raise NotImplementedError('Method hasn\'t been implemented yet')

    def collidepoint(self, *args):
        if len(args) == 1:
            point = args[0]
        elif len(args) == 2:
            point = tuple(args)
        else:
            raise TypeError("argument must contain two numbers")

        return self._collidepoint(point)

    def _collidepoint(self, point):
        raise NotImplementedError('Method hasn\'t been implemented yet')

    def colliderect(self, arg):
        try:
            self.__class__(arg)
        except:
            raise TypeError("Argument must be hitbox style object")

        if 0 in [self.w, self.h, arg.w, arg.h]:
            return False

        if isinstance(arg, Ellipse):
            return self._colliderect_ellipse(Ellipse(arg))
        return self._colliderect_rect(Rect(arg))

    def _colliderect_rect(self, rect):
        raise NotImplementedError('Method hasn\'t been implemented yet')

    def _colliderect_ellipse(self, ellipse):
        raise NotImplementedError('Method hasn\'t been implemented yet')

    def collidelist(self, args):
        for i, arg in enumerate(args):
            if self.colliderect(arg):
                return i

        return -1

    def collidelistall(self, args):
        out = []

        for i, arg in enumerate(args):
            if self.colliderect(arg):
                out.append(i)

        return out

    def collidedict(self, args_dict, use_values=0):
        for key in args_dict:
            if use_values == 0:
                arg = key
            else:
                arg = args_dict[key]

            if self.colliderect(arg):
                return (key, args_dict[key])

        return None  # explicit rather than implicit

    def collidedictall(self, args_dict, use_values=0):
        out = []

        for key in args_dict:
            if use_values == 0:
                arg = key
            else:
                arg = args_dict[key]

            if self.colliderect(arg):
                out.append((key, args_dict[key]))

        return out


class Rect(Hitbox):
    def __str__(self):
        return f"<rect{tuple(self._rect)}>"

    def _clamp_ip_rect(self, rect):
        if self._rect[2] >= rect.w:
            x = rect.x + rect.w / 2 - self._rect[2] / 2
        elif self._rect[0] < rect.x:
            x = rect.x
        elif self._rect[0] + self._rect[2] > rect.x + rect.w:
            x = rect.x + rect.w - self._rect[2]
        else:
            x = self._rect[0]

        if self._rect[3] >= rect.h:
            y = rect.y + rect.h / 2 - self._rect[3] / 2
        elif self._rect[1] < rect.y:
            y = rect.y
        elif self._rect[1] + self._rect[3] > rect.y + rect.h:
            y = rect.y + rect.h - self._rect[3]
        else:
            y = self._rect[1]

        self._rect[0] = x
        self._rect[1] = y

    def _clip_rect(self, rect):
        # left
        if self.x >= rect.x and self.x < rect.x + rect.w:
            x = self.x
        elif rect.x >= self.x and rect.x < self.x + self.w:
            x = rect.x
        else:
            return self.__class__(self.x, self.y, 0, 0)

        # right
        if self.x + self.w > rect.x and self.x + self.w <= rect.x + rect.w:
            w = self.x + self.w - x
        elif (
            rect.x + rect.w > self.x and rect.x + rect.w <= self.x + self.w
        ):
            w = rect.x + rect.w - x
        else:
            return self.__class__(self.x, self.y, 0, 0)

        # top
        if self.y >= rect.y and self.y < rect.y + rect.h:
            y = self.y
        elif rect.y >= self.y and rect.y < self.y + self.h:
            y = rect.y
        else:
            return self.__class__(self.x, self.y, 0, 0)

        # bottom
        if self.y + self.h > rect.y and self.y + self.h <= rect.y + rect.h:
            h = self.y + self.h - y
        elif (
            rect.y + rect.h > self.y and rect.y + rect.h <= self.y + self.h
        ):
            h = rect.y + rect.h - y
        else:
            return self.__class__(self.x, self.y, 0, 0)

        return self.__class__(x, y, w, h)

    def _union_ip_rect(self, rect):
        x = min(self.x, rect.x)
        y = min(self.y, rect.y)
        w = max(self.x + self.w, rect.x + rect.w) - x
        h = max(self.y + self.h, rect.y + rect.h) - y

        self._rect = [x, y, w, h]

    def _fit_rect(self, rect):
        xratio = (self.w / rect.w) if rect.w != 0 else float('inf')
        yratio = (self.h / rect.h) if rect.h != 0 else float('inf')
        maxratio = max(xratio, yratio)

        w = self.w / maxratio
        h = self.h / maxratio

        x = rect.x + (rect.w - w) / 2
        y = rect.y + (rect.h - h) / 2

        return self.__class__(x, y, w, h)

    def _contains_rect(self, rect):
        if self._rect[0] <= rect[0] and rect[0] + rect[2] <= self.right:
            if self._rect[1] <= rect[1] and rect[1] + rect[3] <= self.bottom:
                return True
        return False

    def _contains_ellipse(self, ellipse):
        return self._contains_rect(ellipse)

    def _collidepoint(self, point):
        # conforms with no collision on right / bottom edge behavior of pygame Rects
        if self._rect[0] <= point[0] < self.right:
            if self._rect[1] <= point[1] < self.bottom:
                return True
        return False

    def _colliderect_rect(self, rect):
        return (
            min(self.x, self.x + self.w) < max(rect.x, rect.x + rect.w)
            and min(self.y, self.y + self.h) < max(rect.y, rect.y + rect.h)
            and max(self.x, self.x + self.w) > min(rect.x, rect.x + rect.w)
            and max(self.y, self.y + self.h) > min(rect.y, rect.y + rect.h)
        )

    def _colliderect_ellipse(self, ellipse):
        def f_y(ellipse, x):
            d = 1 - (x - ellipse.centerx)**2 / ellipse.a**2
            return (ellipse.centery - ellipse.b * sqrt(d), ellipse.centery + ellipse.b * sqrt(d)) if d > 0 else ()

        def f_x(ellipse, y):
            d = 1 - (y - ellipse.centery)**2 / ellipse.b**2
            return (ellipse.centerx - ellipse.a * sqrt(d), ellipse.centerx + ellipse.a * sqrt(d)) if d > 0 else ()

        for i in f_x(ellipse, self.top) + f_x(ellipse, self.bottom):
            if self.left <= i < self.right:
                return True

        for i in f_y(ellipse, self.left) + f_y(ellipse, self.right):
            if self.top <= i < self.bottom:
                return True

        return self._contains_ellipse(ellipse)


class Ellipse(Hitbox):
    def __init__(self, *args):
        Hitbox.__init__(self, *args)

        self.getattr_dict.update({
            "a": lambda x: x._rect[2] / 2,
            "b": lambda x: x._rect[3] / 2,
        })

    def __setattr__(self, name, value):
        if name == "a":
            self._rect[2] = value * 2
            return

        if name == "b":
            self._rect[3] = value * 2
            return

        Hitbox.__setattr__(self, name, value)

    @property
    def f1(self):
        if self.a > self.b:
            return (self.centerx - sqrt(self.a**2 - self.b**2), self.centery)
        return (self.centerx, self.centery - sqrt(self.b**2 - self.a**2))

    @property
    def f2(self):
        if self.a > self.b:
            return (self.centerx + sqrt(self.a**2 - self.b**2), self.centery)
        return (self.centerx, self.centery + sqrt(self.b**2 - self.a**2))

    def __str__(self):
        return f"<ellipse{tuple(self._rect)}>"

    def radius(self, alpha):
        return self.a * sin(alpha)**2 + self.b * cos(alpha)**2

    def _contains_rect(self, rect):
        return self.collidepoint(rect.topleft) and self.collidepoint(rect.bottomright)

    def _contains_ellipse(self, ellipse):
        alpha = atan2(ellipse.centery - self.centery, ellipse.centerx - self.centerx)
        beta = pi / 2 - alpha

        return (
            self.collidepoint(ellipse.left, ellipse.centery) and self.collidepoint(ellipse.centerx, ellipse.top)
            and self.collidepoint(ellipse.right, ellipse.centery) and self.collidepoint(ellipse.centerx, ellipse.bottom)
            and sqrt((ellipse.centerx - self.centerx)**2 + (ellipse.centery - self.centery)**2) + ellipse.radius(beta)
            <= self.radius(beta)
        )

    def _collidepoint(self, point):
        if (point[0] - self.centerx)**2 / self.a**2 + (point[1] - self.centery)**2 / self.b**2 <= 1:
            return True
        return False

    def _colliderect_rect(self, rect):
        def f_y(ellipse, x):
            d = 1 - (x - ellipse.centerx)**2 / ellipse.a**2
            return (ellipse.centery - ellipse.b * sqrt(d), ellipse.centery + ellipse.b * sqrt(d)) if d > 0 else ()

        def f_x(ellipse, y):
            d = 1 - (y - ellipse.centery)**2 / ellipse.b**2
            return (ellipse.centerx - ellipse.a * sqrt(d), ellipse.centerx + ellipse.a * sqrt(d)) if d > 0 else ()

        for i in f_x(self, rect.top) + f_x(self, rect.bottom):
            if rect.left <= i < rect.right:
                return True

        for i in f_y(self, rect.left) + f_y(self, rect.right):
            if rect.top <= i < rect.bottom:
                return True

        return self._contains_rect(rect)

    def _colliderect_ellipse(self, ellipse):
        f1, f2 = self.f1, self.f2

        alpha = atan2(ellipse.centery - f1[1], f1[0] - ellipse.centerx)
        beta = pi / 2 - alpha
        r1 = ellipse.radius(beta)
        rx1, ry1 = (ellipse.centerx - -r1 * sin(beta), ellipse.centery + -r1 * cos(beta))
        
        alpha = atan2(ellipse.centery - f2[1], ellipse.centerx - f2[0])
        beta = pi / 2 - alpha
        r2 = ellipse.radius(beta)
        rx2, ry2 = (ellipse.centerx + -r2 * sin(beta), ellipse.centery + -r2 * cos(beta))

        mhaxis = max(self.a, self.b)

        if (
            sqrt((rx1 - f1[0])**2 + (ry1 - f1[1])**2) + sqrt((rx1 - f2[0])**2 + (ry1 - f2[1])**2) <= 2 * mhaxis or
            sqrt((rx2 - f1[0])**2 + (ry2 - f1[1])**2) + sqrt((rx2 - f2[0])**2 + (ry2 - f2[1])**2) <= 2 * mhaxis
        ):
            return True

        f1, f2 = ellipse.f1, ellipse.f2

        alpha = atan2(self.centery - f1[1], f1[0] - self.centerx)
        beta = pi / 2 - alpha
        r1 = self.radius(beta)
        rx1, ry1 = (self.centerx - -r1 * sin(beta), self.centery + -r1 * cos(beta))

        alpha = atan2(self.centery - f2[1], self.centerx - f2[0])
        beta = pi / 2 - alpha
        r2 = self.radius(beta)
        rx2, ry2 = (self.centerx + -r2 * sin(beta), self.centery + -r2 * cos(beta))

        mhaxis = max(ellipse.a, ellipse.b)

        if (
            sqrt((rx1 - f1[0])**2 + (ry1 - f1[1])**2) + sqrt((rx1 - f2[0])**2 + (ry1 - f2[1])**2) <= 2 * mhaxis or
            sqrt((rx2 - f1[0])**2 + (ry2 - f1[1])**2) + sqrt((rx2 - f2[0])**2 + (ry2 - f2[1])**2) <= 2 * mhaxis
        ):
            return True

        return False

