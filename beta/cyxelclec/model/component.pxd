#cython: language_level=3

cdef public int ONLY_ONE = 0b001
cdef public int MANY = 0b010

cdef class Component:
    cdef public bint visible
    cdef public object entity

    cdef void cy_research(self, entity)
    cdef void cy_reset(self)
    cdef void cy_update(self)

    cdef int cy_length_tag(self)
    cdef int cy_hash(self)
