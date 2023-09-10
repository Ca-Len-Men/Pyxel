#cython: language_level=3

from .. cimport component
from ..component cimport Component, MANY

cdef class ComponentScript(Component):
    cdef void cy_update(self)
    cdef void cy_entity_to_canvas(self, canvas)



