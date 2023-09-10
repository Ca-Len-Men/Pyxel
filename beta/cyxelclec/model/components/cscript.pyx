#cython: language_level=3

cdef class ComponentScript(Component):
    #TODO     =====     Cython     =====

    cdef void cy_update(self): pass

    cdef void cy_entity_to_canvas(self, canvas): pass

    #TODO     =====     Pure Python     =====

    def __init__(self, entity):
        Component.__init__(self)
        entity.add_component(self)

    # @abstractmethod
    def update(self):
        self.cy_update()

    def entity_to_canvas(self, canvas):
        self.cy_entity_to_canvas(canvas)

    @classmethod
    def quantity(cls):
        return MANY

    @classmethod
    def get_comp(cls):
        return ComponentScript