#cython: language_level=3

from .. cimport component
from ..component cimport Component

from ...geo cimport fvector
from ...geo.fvector cimport Vector

cdef class ComponentMouseInput(Component):
    cdef object __area
    cdef Vector __touch_pos
    cdef public bint hovered

    cdef public bint pressed_left
    cdef public bint pressed_right
    cdef public bint started_left
    cdef public bint started_right
    cdef public bint ended_left
    cdef public bint ended_right

    cdef public bint pressedin_left
    cdef public bint pressedin_right
    cdef public bint startedin_left
    cdef public bint startedin_right
    cdef public bint endedin_left
    cdef public bint endedin_right

    cdef bint started_dragging
    cdef bint dragging
    cdef bint ended_dragging

cdef class CMouseInput(ComponentMouseInput):
    pass

cdef:
    public int KEY_INPUT = 0b001
    public int NO_KEY_INPUT = 0b010
    public str BACKSPACE = '\x08'

cdef class ComponentKeyInput(Component):
    cdef public int state
    cdef public str char

    cdef void cy_reset(self)
    cdef void cy_update(self)

cdef class CKeyInput(ComponentKeyInput):
    pass
