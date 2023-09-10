#cython: language_level=3

from ..geo cimport fvector
from ..geo.fvector cimport Vector, WeakrefMethod

from ..geo cimport frect
from ..geo.frect cimport Rect, StructRect

from . cimport entity
from .entity cimport Entity

# Khi thay đổi hành vi ( visible, enable ) của một Canvas,
# một lệnh đệ quy tìm qua tất cả các Canvas, Entity có trong `root` để gán lại các `virtual_xxx`
cdef public bint[1] update_behaviour = [False]

class Canvas(Rect):
    cdef public bint automate = False
    cdef public bint __visible = True
    cdef public bint __enable = True
    cdef public bint virtual_visible = True
    cdef public bint virtual_enable = True
    cdef public bint alive = True
    cdef public bint _canvas = None
    cdef public Vector _mouse_position
    cdef public set _entities
    cdef public set _canvases
    cdef public set _remove_set
    cdef public object _sprite

    cdef void cy_init(self)
    cdef void cy_update(self)
    cdef void _cy_render(self)
    cdef void cy_add_entity(self, Entity entity)
    cdef void cy_add_entities(self, list entities)
    cdef void cy_del_entity(self, Entity entity)
    cdef void cy_add_canvas(self, Canvas canvas)
    cdef void cy_add_canvases(self, list canvases)
    cdef void cy_del_canvas(self, Canvas canvas)
    cdef void cy_update_mouse_position(self)
    cdef void cy_update_virtual_behaviour(self)
    cdef void cy_set_canvas(self, Canvas __canvas)
    cdef void cy_set_visible(self, bint __visible)
    cdef void cy_set_enable(self, bint __enable)

    cdef bint cy_get_visible(self)
    cdef bint cy_get_enable(self)
    cdef bint cy_contains(self, item)

    cdef Vector cy_get_mpos(self)
    cdef Canvas cy_get_canvas(self)

cdef public Canvas root = Canvas(None)
