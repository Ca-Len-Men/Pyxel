#cython: language_level=3

from . cimport fvector
from .fvector cimport *

cdef class StructRect:
    cdef Vector _position
    cdef Vector _size

    cdef void cy_set_size(self, Vector __size)
    cdef void cy_set_w(self, double __w)
    cdef void cy_set_h(self, double __h)
    cdef void cy_set_topleft(self, Vector __topleft)
    cdef void cy_set_topright(self, Vector __topright)
    cdef void cy_set_bottomleft(self, Vector __bottomleft)
    cdef void cy_set_bottomright(self, Vector __bottomright)

    cdef bint collide_point(self, Vector point)

    cdef double cy_get_w(self)
    cdef double cy_get_h(self)
    cdef double cy_get_midx(self)
    cdef double cy_get_midy(self)

    cdef Vector cy_get_size(self)
    cdef Vector cy_get_topleft(self)
    cdef Vector cy_get_topright(self)
    cdef Vector cy_get_bottomleft(self)
    cdef Vector cy_get_bottomright(self)

    cdef void cy_set_center(self, Vector __center)
    cdef void cy_set_midtop(self, Vector __midtop)
    cdef void cy_set_midbottom(self, Vector __midbottom)
    cdef void cy_set_midleft(self, Vector __midleft)
    cdef void cy_set_midright(self, Vector __midright)
    cdef void cy_set_midx(self, double __midx)
    cdef void cy_set_midy(self, double __midy)

    cdef Vector cy_get_center(self)
    cdef Vector cy_get_midtop(self)
    cdef Vector cy_get_midbottom(self)
    cdef Vector cy_get_midleft(self)
    cdef Vector cy_get_midright(self)

cdef class Rect(StructRect):
    cdef void cy_size_listener(self, __listener)
    cdef void cy_pos_listener(self, __listener)
    cdef void cy_only_set_size(self, Vector __size)
    cdef void cy_only_set_topleft(self, Vector __topleft)


