#cython: language_level=3

cdef class StructRect:
    #TODO     =====     Cython     =====
    
    cdef fvector.Vector cy_get_size(self):
        return self._size.cy_copy()

    cdef void cy_set_size(self, fvector.Vector __size):
        self._size.cy_set(__size)

    cdef double cy_get_w(self):
        return self._size.__x

    cdef void cy_set_w(self, double __w):
        self._size.x = __w

    cdef double cy_get_h(self):
        return self._size.__y

    cdef void cy_set_h(self, double __h):
        self._size.y = __h

    cdef fvector.Vector cy_get_topleft(self):
        return self._position.cy_copy()

    cdef void cy_set_topleft(self, fvector.Vector __topleft):
        self._position.cy_set(__topleft)

    cdef fvector.Vector cy_get_topright(self):
        cdef fvector.Vector __topleft = self.cy_get_topleft()
        return fvector.Vector(__topleft.__x + self._size.__x - 1, __topleft.__y)

    cdef void cy_set_topright(self, fvector.Vector __topright):
        self.cy_set_topleft(fvector.Vector(__topright.__x - self._size.__x + 1, __topright.__y))

    cdef fvector.Vector cy_get_bottomleft(self):
        cdef fvector.Vector __topleft = self.cy_get_topleft()
        return fvector.Vector(__topleft.__x, __topleft.__y + self._size.__y - 1)

    cdef void cy_set_bottomleft(self, fvector.Vector __bottomleft):
        self.cy_set_topleft(fvector.Vector(__bottomleft.__x, __bottomleft.__y - self._size.__y + 1))

    cdef fvector.Vector cy_get_bottomright(self):
        cdef fvector.Vector __topleft = self.cy_get_topleft()
        return fvector.Vector(__topleft.__x + self._size.__x - 1, __topleft.__y + self._size.__y - 1)

    cdef void cy_set_bottomright(self, fvector.Vector __bottomright):
        self.cy_set_topleft(
            fvector.Vector(__bottomright.__x - self._size.__x + 1, __bottomright.__y - self._size.__y + 1))

    cdef fvector.Vector cy_get_center(self):
        cdef fvector.Vector __topleft = self.cy_get_topleft()
        return fvector.Vector(__topleft.__x + self._size.__x / 2, __topleft.__y + self._size.__y / 2)

    cdef void cy_set_center(self, fvector.Vector __center):
        self.cy_set_topleft(fvector.Vector(__center.__x - self._size.__x / 2, __center.__y - self._size.__y / 2))

    cdef fvector.Vector cy_get_midtop(self):
        cdef fvector.Vector __topleft = self.cy_get_topleft()
        return fvector.Vector(__topleft.__x + self._size.__x / 2, __topleft.__y)

    cdef void cy_set_midtop(self, fvector.Vector __midtop):
        self.cy_set_topleft(fvector.Vector(__midtop.__x - self._size.__x / 2, __midtop.__y))

    cdef fvector.Vector cy_get_midbottom(self):
        cdef fvector.Vector __topleft = self.cy_get_topleft()
        return fvector.Vector(__topleft.__x + self._size.__x / 2, __topleft.__y + self._size.__y - 1)

    cdef void cy_set_midbottom(self, fvector.Vector __midbottom):
        self.cy_set_topleft(fvector.Vector(__midbottom.__x - self._size.__x / 2, __midbottom.__y - self._size.__y + 1))

    cdef fvector.Vector cy_get_midleft(self):
        cdef fvector.Vector __topleft = self.cy_get_topleft()
        return fvector.Vector(__topleft.__x, __topleft.__y + self._size.__y / 2)

    cdef void cy_set_midleft(self, fvector.Vector __midleft):
        self.cy_set_topleft(fvector.Vector(__midleft.__x, __midleft.__y - self._size.__y / 2))

    cdef fvector.Vector cy_get_midright(self):
        cdef fvector.Vector __topleft = self.cy_get_topleft()
        return fvector.Vector(__topleft.__x + self._size.__x - 1, __topleft.__y + self._size.__y / 2)

    cdef void cy_set_midright(self, fvector.Vector __midright):
        self.cy_set_topleft(fvector.Vector(__midright.__x - self._size.__x + 1, __midright.__y - self._size.__y / 2))

    cdef double cy_get_midx(self):
        return self._position.__x + self._size.__x / 2

    cdef void cy_set_midx(self, double __midx):
        self.cy_set_topleft(fvector.Vector(__midx - self._size.__x / 2, self._position.__y))

    cdef double cy_get_midy(self):
        return self._position.__y + self._size.__y / 2

    cdef void cy_set_midy(self, double __midy):
        self.cy_set_topleft(fvector.Vector(self._position.__x, __midy - self._size.__y / 2))

    cdef bint collide_point(self, fvector.Vector point):
        return self._position.__x <= point.__x < (self._position.__x + self._size.__x) and \
            self._position.__y <= point.__y < (self._position.__y + self._size.__y)

    #TODO     =====     Pure Python     =====
    
    def __init__(self, fvector.Vector size, fvector.Vector position=None):
        if position is None:
            self._position = fvector.Vector(0, 0)
        else:
            self._position = position
        self._size = size

    @property
    def size(self):
        return self._size.cy_copy()

    @size.setter    # type: ignore
    def size(self, fvector.Vector __size):
        self._size.cy_set(__size)

    @property
    def w(self):
        return self._size.__x

    @w.setter   # type: ignore
    def w(self, double __w):
        self._size.x = __w

    @property
    def h(self):
        return self._size.__y

    @h.setter   # type: ignore
    def h(self, double __h):
        self._size.y = __h

    @property
    def topleft(self):
        return self._position.cy_copy()

    @topleft.setter # type: ignore
    def topleft(self, fvector.Vector __topleft):
        self._position.cy_set(__topleft)

    @property
    def topright(self):
        cdef fvector.Vector __topleft = self.topleft
        return fvector.Vector(__topleft.__x + self._size.__x - 1, __topleft.__y)

    @topright.setter    # type: ignore
    def topright(self, fvector.Vector __topright):
        self.topleft = fvector.Vector(__topright.__x - self._size.__x + 1, __topright.__y)

    @property
    def bottomleft(self):
        cdef fvector.Vector __topleft = self.topleft
        return fvector.Vector(__topleft.__x, __topleft.__y + self._size.__y - 1)

    @bottomleft.setter  # type: ignore
    def bottomleft(self, fvector.Vector __bottomleft):
        self.topleft = fvector.Vector(__bottomleft.__x, __bottomleft.__y - self._size.__y + 1)

    @property
    def bottomright(self):
        cdef fvector.Vector __topleft = self.topleft
        return fvector.Vector(__topleft.__x + self._size.__x - 1, __topleft.__y + self._size.__y - 1)

    @bottomright.setter # type: ignore
    def bottomright(self, fvector.Vector __bottomright):
        self.topleft = fvector.Vector(__bottomright.__x - self._size.__x + 1, __bottomright.__y - self._size.__y + 1)

    @property
    def center(self):
        cdef fvector.Vector __topleft = self.topleft
        return fvector.Vector(__topleft.__x + self._size.__x / 2, __topleft.__y + self._size.__y / 2)

    @center.setter  # type: ignore
    def center(self, fvector.Vector __center):
        self.topleft = fvector.Vector(__center.__x - self._size.__x / 2, __center.__y - self._size.__y / 2)

    @property
    def midtop(self):
        cdef fvector.Vector __topleft = self.topleft
        return fvector.Vector(__topleft.__x + self._size.__x / 2, __topleft.__y)

    @midtop.setter  # type: ignore
    def midtop(self, fvector.Vector __midtop):
        self.topleft = fvector.Vector(__midtop.__x - self._size.__x / 2, __midtop.__y)

    @property
    def midbottom(self):
        cdef fvector.Vector __topleft = self.topleft
        return fvector.Vector(__topleft.__x + self._size.__x / 2, __topleft.__y + self._size.__y - 1)

    @midbottom.setter   # type: ignore
    def midbottom(self, fvector.Vector __midbottom):
        self.topleft = fvector.Vector(__midbottom.__x - self._size.__x / 2, __midbottom.__y - self._size.__y + 1)

    @property
    def midleft(self):
        cdef fvector.Vector __topleft = self.topleft
        return fvector.Vector(__topleft.__x, __topleft.__y + self._size.__y / 2)

    @midleft.setter # type: ignore
    def midleft(self, fvector.Vector __midleft):
        self.topleft = fvector.Vector(__midleft.__x, __midleft.__y - self._size.__y / 2)

    @property
    def midright(self):
        cdef fvector.Vector __topleft = self.topleft
        return fvector.Vector(__topleft.__x + self._size.__x - 1, __topleft.__y + self._size.__y / 2)

    @midright.setter    # type: ignore
    def midright(self, fvector.Vector __midright):
        self.topleft = fvector.Vector(__midright.__x - self._size.__x + 1, __midright.__y - self._size.__y / 2)

    @property
    def midx(self):
        return self._position.__x + self._size.__x / 2

    @midx.setter    # type: ignore
    def midx(self, double __midx):
        self.topleft = fvector.Vector(__midx - self._size.__x / 2, self._position.__y)

    @property
    def midy(self):
        return self._position.__y + self._size.__y / 2

    @midy.setter    # type: ignore
    def midy(self, double __midy):
        self.topleft = fvector.Vector(self._position.__x, __midy - self._size.__y / 2)

    def __str__(self):
        return f'Rect({self._position}-{self._size})'

    def __repr__(self):
        return self.__str__()

cdef class Rect(StructRect):
    #TODO     =====     Cython     =====

    cdef void cy_size_listener(self, __listener):
        self._size.add_listener(__listener)

    cdef void cy_pos_listener(self, __listener):
        self._position.add_listener(__listener)

    cdef void cy_only_set_size(self, fvector.Vector __size):
        cdef fvector.VectorListener __self_size = <fvector.VectorListener> self._size
        __self_size.cy_only_set(__size)

    cdef void cy_only_set_topleft(self, fvector.Vector __topleft):
        cdef fvector.VectorListener __self_topleft = <fvector.VectorListener> self._position
        __self_topleft.cy_only_set(__topleft)

    #TODO     =====     Pure Python     =====

    def __init__(self, fvector.Vector size, fvector.Vector position=None):
        cdef fvector.Vector __position
        if position is None:
            __position = fvector.VectorListener(position.__x, position.__y)
        else:
            __position = fvector.VectorListener(0, 0)
        super().__init__(size, __position)
