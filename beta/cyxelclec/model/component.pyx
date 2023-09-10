#cython: language_level=3

from abc import abstractmethod

cdef class Component:
    #TODO     =====     Cython     =====

    cdef void cy_research(self, entity): pass
    cdef void cy_reset(self): pass
    cdef void cy_update(self): pass

    cdef int cy_length_tag(self):
        return self.__class__.quantity()

    cdef int cy_hash(self):
        return id(self.__class__.get_comp())

    #TODO     =====     Pure Python     =====

    def __init__(self):
        self.visible = True
        self.entity = None

    def research(self, entity): pass
    def reset(self): pass
    def update(self): pass

    def length_tag(self):
        return self.__class__.quantity()

    @classmethod
    @abstractmethod
    def get_comp(cls): pass

    @classmethod
    def quantity(cls):
        return ONLY_ONE

    def __hash__(self):
        return self.cy_hash()


