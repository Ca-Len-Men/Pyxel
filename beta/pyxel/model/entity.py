# /**************************************************************************/
# /*  entity.py                                                             */
# /**************************************************************************/
# /*                         This file is part of:                          */
# /*                                 PYXEL                                  */
# /*                  https://github.com/Ca-Len-Men/Pyxel                   */
# /**************************************************************************/

"""
- Entity là các GameObject trong trò chơi.
- Một Entity có thể chứa nhiều Component cần thiết để tạo nên đặc điểm của GameObject.
- Các Component trong Entity là động, có thể xem, thêm, xóa trong lúc trò chơi đang chạy.
"""

from pyxel.struct.pvector import Vector
from pyxel.struct.prect import Rect
from pyxel.model.component import Component, ONLY_ONE
from pyxel.model.components.script import ComponentScript
from pyxel.system_warning import warning_report

class ComponentStorage:
    """ Nơi lưu trữ nhiều Component các loại. """

    def __init__(self):
        self.__scripts = None
        self.__storage = {}

    def add_component(self, component: Component) -> None:
        component.entity = self

        # Adding this component to dictionary.
        hash_ = component.__hash__()

        if component.quantity() == ONLY_ONE:
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

    def add_components(self, *components) -> None:
        """Adding components into this storage."""
        for component in components:
            self.add_component(component)

    def get_component(self, __component_class, *, get_all=False):
        """ Lấy ``Component`` với kiểu được chỉ định.

        :param __component_class: một lớp Component với tiền tố là ``ComponentXXX``
        :param get_all: True nếu muốn lấy hết ``Component`` cùng kiểu
        :return: thể hiện của lớp truyền vào
        """

        # Nếu Component cần lấy là Script -> bỏ qua `get_all`,
        # chỉ trả về duy nhất thể hiện của ComponentScript
        hash_ = id(__component_class)
        if issubclass(__component_class, ComponentScript):
            return self.__scripts.get(hash_)

        val_ = self.__storage.get(hash_)
        if isinstance(val_, list) and not get_all:
            return val_[0]
        return val_

    def get_components(self, *__component_classes):
        """ Lấy ra cùng lúc nhiều kiểu ``Component``.

        :return: một ``tuple`` các ``Component``, thứ tự giữ nguyên.
        """

        return tuple(self.get_component(__component_class)
                     for __component_class in __component_classes)

    def del_component(self, __component_class, *, remove_all=False) -> None:
        """ Xóa ``ComponentScript`` khỏi ``Entity``.

        - Nếu tham số **__component_class** là ``ComponentScript`` -> xóa toàn bộ script.
        - Nếu là subclass của ``ComponentScript`` -> chỉ xóa script tương ứng.
        - Các loại ``Component`` khác, nếu ``Component.quantity``  là ``MANY`` và **remove_all** là ``True`` thì xóa toàn bộ.
        - Ngược lại, chỉ xóa một hoặc xóa ``ComponentScript`` đứng đầu trong ``list``.

        :return:
        """

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
        warning_report.add(self)
        super().__init__()
        self.__visible = True
        self.__enable = True
        self.virtual_visible = True
        self.virtual_enable = True

        self.alive = True
        self.automate = False
        self._canvas = None
        self._rect = None

    def warning(self):
        if self.canvas is None:
            print(f'Warning: {str(self)} chưa được gán vào Canvas !')

    def reset(self):
        for component in self.components:
            component.reset()

    def update(self):
        for script in self.scripts:
            script.update()

    def re_structured(self):
        """Re-structured all components in this entity."""

        for comp in self.components:
            comp.research(self)

    def _adding_to_canvas(self):
        """ Chỉ được gọi khi ``Entity`` được thêm vào ``Canvas``
        :return:"""

        for script in self.scripts:
            script.entity_to_canvas(self.canvas)

    @property
    def rect(self):
        if self._rect is None:
            self._rect = Rect(Vector(0, 0))
        return self._rect

    @property
    def canvas(self):
        return self._canvas

    @canvas.setter  # type: ignore
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

    @visible.setter  # type: ignore
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

    @enable.setter  # type: ignore
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
