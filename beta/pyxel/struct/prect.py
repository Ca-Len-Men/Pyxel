# /**************************************************************************/
# /*  prect.py                                                              */
# /**************************************************************************/
# /*                         This file is part of:                          */
# /*                                 PYXEL                                  */
# /*                  https://github.com/Ca-Len-Men/Pyxel                   */
# /**************************************************************************/

from pyxel.struct.pvector import Vector

class Rect:
    def __init__(self, size, position=None):
        if position is None:
            self.__position = Vector(0, 0)
        else:
            self.__position = position
        self.__size = size

    def collide_point(self, point: Vector):
        return self.__position.x <= point.x < (self.__position.x + self.w) and \
            self.__position.y <= point.y < (self.__position.y + self.h)

    def get_position(self):
        return self.__position

    def get_size(self):
        return self.__size

    @property
    def size(self):
        return self.__size.copy()

    @size.setter    # type: ignore
    def size(self, __size: Vector):
        self.__size.set(__size)

    @property
    def w(self):
        return self.__size.x

    @w.setter   # type: ignore
    def w(self, __w: float):
        self.size = Vector(__w, self.h)

    @property
    def h(self):
        return self.__size.y

    @h.setter   # type: ignore
    def h(self, __h: float):
        self.size = Vector(self.w, __h)

    @property
    def topleft(self):
        return self.__position.copy()

    @topleft.setter # type: ignore
    def topleft(self, __topleft):
        self.__position.set(__topleft)

    @property
    def topright(self):
        __topleft = self.topleft
        return Vector(__topleft.x + self.w - 1, __topleft.y)

    @topright.setter    # type: ignore
    def topright(self, __topright: Vector):
        self.topleft = Vector(__topright.x - self.w + 1, __topright.y)

    @property
    def bottomleft(self):
        __topleft = self.topleft
        return Vector(__topleft.x, __topleft.y + self.h - 1)

    @bottomleft.setter  # type: ignore
    def bottomleft(self, __bottomleft: Vector):
        self.topleft = Vector(__bottomleft.x, __bottomleft.y - self.h + 1)

    @property
    def bottomright(self):
        __topleft = self.topleft
        return Vector(__topleft.x + self.w - 1, __topleft.y + self.h - 1)

    @bottomright.setter # type: ignore
    def bottomright(self, __bottomright: Vector):
        self.topleft = Vector(__bottomright.x - self.w + 1, __bottomright.y - self.h + 1)

    @property
    def center(self):
        __topleft = self.topleft
        return Vector(__topleft.x + self.w / 2, __topleft.y + self.h / 2)

    @center.setter  # type: ignore
    def center(self, __center):
        self.topleft = Vector(__center.x - self.w / 2, __center.y - self.h / 2)

    @property
    def midtop(self):
        __topleft = self.topleft
        return Vector(__topleft.x + self.w / 2, __topleft.y)

    @midtop.setter  # type: ignore
    def midtop(self, __midtop: Vector):
        self.topleft = Vector(__midtop.x - self.w / 2, __midtop.y)

    @property
    def midbottom(self):
        __topleft = self.topleft
        return Vector(__topleft.x + self.w / 2, __topleft.y + self.h - 1)

    @midbottom.setter   # type: ignore
    def midbottom(self, __midbottom: Vector):
        self.topleft = Vector(__midbottom.x - self.w / 2, __midbottom.y - self.h + 1)

    @property
    def midleft(self):
        __topleft = self.topleft
        return Vector(__topleft.x, __topleft.y + self.h / 2)

    @midleft.setter # type: ignore
    def midleft(self, __midleft: Vector):
        self.topleft = Vector(__midleft.x, __midleft.y - self.h / 2)

    @property
    def midright(self):
        __topleft = self.topleft
        return Vector(__topleft.x + self.w - 1, __topleft.y + self.h / 2)

    @midright.setter    # type: ignore
    def midright(self, __midright: Vector):
        self.topleft = Vector(__midright.x - self.w + 1, __midright.y - self.h / 2)

    @property
    def midx(self):
        return self.__position.x + self.w / 2

    @midx.setter    # type: ignore
    def midx(self, __midx: Vector):
        self.topleft = Vector(__midx - self.w / 2, self.__position.y)

    @property
    def midy(self):
        return self.__position.y + self.h / 2

    @midy.setter    # type: ignore
    def midy(self, __midy: Vector):
        self.topleft = Vector(self.__position.x, __midy - self.h / 2)

    def __str__(self):
        return f'Rect({self.__position}-{self.__size})'

    def __repr__(self):
        return self.__str__()