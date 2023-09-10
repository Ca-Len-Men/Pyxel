from pyxelclec.model.component import ONLY_ONE
from pyxelclec.model.components.ccollider import ComponentCollider
from pyxelclec.model.components.cscript import ComponentScript

class ComponentStorage:
    def __init__(self):
        self.__scripts = None
        self.__storage = {}

    def add_component(self, component):
        """ Adding a component into this storage."""

        # Let's component searched in this entity.
        # component.add_to_entity(self)
        component.entity = self
        # Adding this component to dictionary.
        hash_ = component.__hash__()

        if component.length_tag() == ONLY_ONE:
            self.__storage[hash_] = component
        else:
            # Script type saving on 'self.__scripts'
            if issubclass(component.__class__, ComponentScript):
                if self.__scripts is None:
                    self.__scripts = {}
                hash_ = id(component.__class__)
                self.__scripts[hash_] = component
            else:
                if hash_ not in self.__storage:
                    self.__storage[hash_] = []
                self.__storage[hash_].append(component)

    def add_components(self, *components):
        """Adding components into this storage."""
        for component in components:
            self.add_component(component)

    def get_component(self, __component_class, *, get_all=False):
        hash_ = id(__component_class)
        if issubclass(__component_class, ComponentScript):
            return self.__scripts.get(hash_)

        val_ = self.__storage.get(hash_)
        if isinstance(val_, list) and not get_all:
            return val_[0]
        return val_

    def get_components(self, *__component_classes):
        return tuple(self.get_component(__component_class)
                     for __component_class in __component_classes)

    def del_component(self, __component_class, remove_all=False):
        if __component_class is ComponentScript:
            self.__scripts = None
            return

        hash_ = id(__component_class)
        if issubclass(__component_class, ComponentScript):
            del self.__scripts[hash_]
            return

        val_ = self.__storage.get(hash_)
        if val_ is None:
            return
        
        if isinstance(val_, list) and remove_all:
            del self.__storage[hash_]
            return
        del self.__storage[hash_]

    @property
    def components(self):
        for comp in self.__storage.values():
            if isinstance(comp, list):
                for __comp in comp:
                    yield __comp
            else:
                yield comp
        if self.__scripts:
            for script in self.__scripts.values():
                yield script

    @property
    def scripts(self):
        if self.__scripts:
            for component_script in self.__scripts.values():
                yield component_script

class Entity(ComponentStorage):
    def __init__(self):
        super().__init__()
        self.automate = False
        self.__visible = True
        self.__enable = True
        self.virtual_visible = True
        self.virtual_enable = True
        self.alive = True
        self._canvas = None
        self._component_area = None

    def reset(self):
        for component in self.components:
            component.system_mode(False)
            component.reset()

    def update(self):
        for script in self.scripts:
            script.update()

    def re_structured(self):
        """Re-structured all components in this entity."""

        for comp in self.components:
            comp.research(self)

    def _adding_to_canvas(self):
        for script in self.scripts:
            script.entity_to_canvas(self.canvas)

    @property
    def collider(self):
        if self._component_area is None:
            self._component_area = self.get_component(ComponentCollider)
        return self._component_area

    @property
    def canvas(self):
        return self._canvas

    @canvas.setter
    def canvas(self, __canvas):
        if self._canvas:
            return

        # Nếu nó được thêm vào trong canvas -> gán `_canvas`
        if self in __canvas:
            self._canvas = __canvas
            self._adding_to_canvas()

    @property
    def visible(self):
        return self.__visible

    @visible.setter
    def visible(self, __visible):
        self.__visible = __visible
        if not __visible:
            self.virtual_visible = False
            return
        # Nếu `__visible` là True -> cần kiểm tra có nên gán virutal_visible = True hay không
        # -> Tìm lên các Canvas chứa nó, nếu tồn tại Canvas có visible = False,
        # gán virutal_visible = False
        # Ngược lại, toàn bộ Canvas phía trên có visible = True -> gán virutal_visible = True
        __node = self
        while __node := __node.canvas:
            # Nếu tồn tại Canvas.visible == False
            if not __node.visible:
                self.virtual_visible = False
                return

    @property
    def enable(self):
        return self.__enable

    @enable.setter
    def enable(self, __enable):
        self.__enable = __enable
        if not __enable:
            self.virtual_enable = False
            return
        # Tương tự như gán visible ( xem phía trên )

        __node = self
        while __node := __node.canvas:
            # Nếu tồn tại Canvas.visible == False
            if not __node.enable:
                self.virtual_enable = False
                return
