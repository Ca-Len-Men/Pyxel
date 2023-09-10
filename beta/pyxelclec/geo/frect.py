from .fvector import *

class StructRect:
    def __init__(self, size, position=None):
        if position is None:
            self._position = Vector.zero()
        else:
            self._position = position
        self._size = size

    def collide_point(self, point):
        return self._position.x <= point.x < (self._position.x + self._size.x) and \
            self._position.y <= point.y < (self._position.y + self._size.y)

    @property
    def size(self):
        return self._size.copy()

    @size.setter    # type: ignore
    def size(self, __size):
        self._size.set(__size)

    @property
    def w(self):
        return self._size.x

    @w.setter   # type: ignore
    def w(self, __w):
        self._size.x = __w

    @property
    def h(self):
        return self._size.y

    @h.setter   # type: ignore
    def h(self, __h):
        self._size.y = __h

    @property
    def topleft(self):
        return self._position.copy()

    @topleft.setter # type: ignore
    def topleft(self, __topleft):
        self._position.set(__topleft)

    @property
    def topright(self):
        __topleft = self.topleft
        return Vector(__topleft.x + self._size.x - 1, __topleft.y)

    @topright.setter    # type: ignore
    def topright(self, __topright):
        self.topleft = Vector(__topright.x - self._size.x + 1, __topright.y)

    @property
    def bottomleft(self):
        __topleft = self.topleft
        return Vector(__topleft.x, __topleft.y + self._size.y - 1)

    @bottomleft.setter  # type: ignore
    def bottomleft(self, __bottomleft):
        self.topleft = Vector(__bottomleft.x, __bottomleft.y - self._size.y + 1)

    @property
    def bottomright(self):
        __topleft = self.topleft
        return Vector(__topleft.x + self._size.x - 1, __topleft.y + self._size.y - 1)

    @bottomright.setter # type: ignore
    def bottomright(self, __bottomright):
        self.topleft = Vector(__bottomright.x - self._size.x + 1, __bottomright.y - self._size.y + 1)

    @property
    def center(self):
        __topleft = self.topleft
        return Vector(__topleft.x + self._size.x / 2, __topleft.y + self._size.y / 2)

    @center.setter  # type: ignore
    def center(self, __center):
        self.topleft = Vector(__center.x - self._size.x / 2, __center.y - self._size.y / 2)

    @property
    def midtop(self):
        __topleft = self.topleft
        return Vector(__topleft.x + self._size.x / 2, __topleft.y)

    @midtop.setter  # type: ignore
    def midtop(self, __midtop):
        self.topleft = Vector(__midtop.x - self._size.x / 2, __midtop.y)

    @property
    def midbottom(self):
        __topleft = self.topleft
        return Vector(__topleft.x + self._size.x / 2, __topleft.y + self._size.y - 1)

    @midbottom.setter   # type: ignore
    def midbottom(self, __midbottom):
        self.topleft = Vector(__midbottom.x - self._size.x / 2, __midbottom.y - self._size.y + 1)

    @property
    def midleft(self):
        __topleft = self.topleft
        return Vector(__topleft.x, __topleft.y + self._size.y / 2)

    @midleft.setter # type: ignore
    def midleft(self, __midleft):
        self.topleft = Vector(__midleft.x, __midleft.y - self._size.y / 2)

    @property
    def midright(self):
        __topleft = self.topleft
        return Vector(__topleft.x + self._size.x - 1, __topleft.y + self._size.y / 2)

    @midright.setter    # type: ignore
    def midright(self, __midright):
        self.topleft = Vector(__midright.x - self._size.x + 1, __midright.y - self._size.y / 2)

    @property
    def midx(self):
        return self._position.x + self._size.x / 2

    @midx.setter    # type: ignore
    def midx(self, __midx):
        self.topleft = Vector(__midx - self._size.x / 2, self._position.y)

    @property
    def midy(self):
        return self._position.y + self._size.y / 2

    @midy.setter    # type: ignore
    def midy(self, __midy):
        self.topleft = Vector(self._position.x, __midy - self._size.y / 2)

    def __str__(self):
        return f'Rect({self._position}-{self._size})'

    def __repr__(self):
        return self.__str__()

class Rect(StructRect):
    def __init__(self, size, position=None):    # type: ignore
        if position:
            self._position = VectorListener(position.x, position.y)
        else:
            self._position = VectorListener(0, 0)
        self._size = VectorListener(size.x, size.y)

    def size_listener(self, __listener):
        self._size.add_listener(__listener)

    def pos_listener(self, __listener):
        self._position.add_listener(__listener)

    def only_set_size(self, __size):
        self._size.only_set(__size)

    def only_set_topleft(self, __topleft):
        self._position.only_set(__topleft)


