from pyxelclec.model.component import Component, MANY

from abc import ABC, abstractmethod

class ComponentScript(ABC, Component):
    def __init__(self, entity):
        Component.__init__(self)
        entity.add_component(self)

    @abstractmethod
    def update(self): pass

    def entity_to_canvas(self, canvas): pass

    @classmethod
    def quantity(cls):
        return MANY

    @classmethod
    def get_comp(cls):
        return ComponentScript