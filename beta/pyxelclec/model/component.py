from abc import abstractmethod

ONLY_ONE = 0b001
MANY = 0b010

class Component:
    @classmethod
    @abstractmethod
    def get_comp(cls): pass

    def __init__(self):
        self.visible = True
        self.entity = None

    def research(self, entity): pass
    def reset(self): pass
    def update(self): pass

    def length_tag(self):
        return self.__class__.quantity()

    @classmethod
    def quantity(cls):
        return ONLY_ONE

    def __hash__(self):
        return id(self.__class__.get_comp())