# /**************************************************************************/
# /*  script.py                                                             */
# /**************************************************************************/
# /*                         This file is part of:                          */
# /*                                 PYXEL                                  */
# /*                  https://github.com/Ca-Len-Men/Pyxel                   */
# /**************************************************************************/

from pyxel.model.component import Component, MANY

class ComponentScript(Component):
    def __init__(self, entity):
        Component.__init__(self)
        entity.add_component(self)

    def update(self):
        """ Được gọi liên tục mỗi vòng lặp. """

    def entity_to_canvas(self, canvas):
        """ Chỉ được gọi khi ``Entity`` chứa nó được thêm vào ``Canvas``.
        :return:"""
        pass

    def quantity(self) -> int:
        return MANY

    def __hash__(self):
        return id(ComponentScript)
