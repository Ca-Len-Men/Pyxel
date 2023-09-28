# /**************************************************************************/
# /*  control.py                                                            */
# /**************************************************************************/
# /*                         This file is part of:                          */
# /*                                 PYXEL                                  */
# /*                  https://github.com/Ca-Len-Men/Pyxel                   */
# /**************************************************************************/

from pyxel.model.components.script import ComponentScript
from pyxel.model.components.user_input import CMouseInput
from pyxel.model.entity import Entity

"""
Các trạng thái của button :
    - Hovered : chuột nằm trong collider của button.
    - Pressed : nhấn giữ chuột liên tục.
    - Clicked : nhấn và thả chuột ngay lập tức ( chuột trái ).
    - Normalized
    
- (!) : một thời điểm chỉ có duy nhất một trạng thái xảy ra
"""

class ButtonScript(ComponentScript):
    """ Abstract class. """

    def __init__(self, collider, *, entity=None):
        if entity is None:
            entity = Entity()
        super().__init__(entity)
        self._collider = collider
        # collider.visible = True
        self._mouse_input = CMouseInput()
        self._mouse_input.set_collider(collider)
        entity.add_components(self._collider, self._mouse_input)

    @property
    def mouse_input(self):
        return self._mouse_input

class ButtonNormal(ButtonScript):
    """ Abstract class. """

    def update(self):
        self.mouse_input.update()
        if not self.entity.virtual_visible:
            self.mouse_input.reset()
            return

        self._collider.update()
        _enable = self.entity.virtual_enable
        if not _enable:
            self.mouse_input.reset()

        if self.mouse_input.startedin_left:
            if _enable:
                self._clicked()
        elif self.mouse_input.pressedin_left:
            if _enable:
                self._pressed()
        elif self.mouse_input.hovered:
            self._hovered()
        else:
            self._normalized()

    def _hovered(self): pass
    def _pressed(self): pass
    def _clicked(self): pass
    def _normalized(self): pass
