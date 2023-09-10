from pyxelclec.__flag__ import FLAG_NO_RENDER
from pyxelclec.geo.imagine import *
from pyxelclec.model.components.cscript import ComponentScript
from pyxelclec.model.components.ccollider import CRect
from pyxelclec.model.components.cinput import CMouseInput
from pyxelclec.model.components.csprite import CSprite, CLabel

from abc import ABC

class ButtonScript(ComponentScript, ABC):
    def __init__(self, entity, collider):
        super().__init__(entity)
        self._collider = collider
        self._mouse_input = CMouseInput()
        entity.add_components(self._collider, self._mouse_input)

    @property
    def minput(self):
        return self._mouse_input

    @property
    def collider(self):
        return self._collider

class ButtonBootstrap(ButtonScript):
    _keys = {'width', 'size'}
    keys = _keys | CLabel.keys | keys_border_radius

    def __init__(self, entity, **kwargs):
        self._keys_border_radius = {'border': 8}
        self._width = 2
        self._size = None
        self._label = CLabel(enhance_opacity=2)
        self._first_sprite = CSprite()
        self._second_sprite = CSprite()

        super().__init__(entity, CRect(0, 0))
        entity.add_components(self._first_sprite, self._second_sprite)
        entity.re_structured()
        self.set(**kwargs)

    def set(self, **kwargs):
        if not kwargs:
            self._render_source()
            return

        __flag_no_render = False
        if FLAG_NO_RENDER in kwargs:
            __flag_no_render = True
            del kwargs[FLAG_NO_RENDER]

        self._label.set(**kwargs)

        __keys = keys_border_radius.intersection(kwargs)
        if __keys:
            self._keys_border_radius.clear()
            for key in __keys:
                self._keys_border_radius[key] = kwargs[key]

        __keys = ButtonBootstrap.keys.intersection(kwargs)
        if __keys:
            for key in __keys:
                setattr(self, f'_{key}', kwargs[key])

        if not __flag_no_render:
            self._render_source()
        return self

    def _render_source(self):
        __CONSTANT_PADDING = self._label.h * .6
        size = self._size
        if size is None:
            size = self._label.size + Vector(__CONSTANT_PADDING, __CONSTANT_PADDING)

        first_rounded = rect_width(size, self._label.color, self._width,
                                                  **self._keys_border_radius)
        second_rounded = rect(size, self._label.color,
                                             **self._keys_border_radius)

        self._first_sprite.surface = new_surface(size)
        self._second_sprite.surface = new_surface(size)

        self._first_sprite.blit(first_rounded, (0, 0))
        self._first_sprite.blit(self._label.surfconst, 'center')
        self._second_sprite.blit(second_rounded, (0, 0))
        self._second_sprite.sub(self._label, 'center')

        self.collider.size = size

    def update(self):
        self.minput.update()

        if not self.entity.virtual_visible:
            self.minput.reset()
            return

        if not self.entity.virtual_enable:
            self._first_sprite.update()
            self.minput.reset()
            return

        if self.minput.hovered:
            self._second_sprite.update()
        else:
            self._first_sprite.update()

class ButtonIcon(ButtonScript):
    keys = {'size'}

    def __init__(self, entity, icon, *, collider=CRect(0, 0)):
        self._icon = CSprite(icon)
        self._icon_filled = CSprite()

        if collider.size.tup_int == (0, 0):
            collider.only_set_size(self._icon.size)

        entity.add_components(self._icon, self._icon_filled)
        super().__init__(entity, collider)
        entity.re_structured()
        self._render_source()

    def _render_source(self):
        self._icon.size = self.collider.size
        self._icon_filled.surface = self._icon.surfconst.copy()
        self._icon_filled.fill(Color.White.rgb, 100)

    def update(self):
        self.minput.update()
        if not self.entity.virtual_visible:
            self.minput.reset()
            return

        self._icon.update()
        if not self.entity.virtual_enable:
            self.minput.reset()
            return

        if self.minput.hovered:
            self._icon_filled.update()

class ButtonState(ButtonScript):
    keys = {'size'}

    def __init__(self, entity, first_state_icon, second_state_icon, *, collider=CRect(0, 0)):
        self.state = False
        self._first_state_icon = CSprite(first_state_icon)
        self._first_state_filled = CSprite()
        self._second_state_icon = CSprite(second_state_icon)
        self._second_state_filled = CSprite()

        if collider.size.tup_int == (0, 0):
            collider.only_set_size(self._first_state_icon.size)

        # area.visible = True
        entity.add_components(self._first_state_icon, self._second_state_icon,
                              self._first_state_filled, self._second_state_filled)
        super().__init__(entity, collider)
        entity.re_structured()
        self._render_source()

    def set(self, **kwargs):
        if not kwargs:
            self._render_source()
            return

        __value = kwargs.get('size')
        if __value:
            self.collider.size = __value

        if FLAG_NO_RENDER not in kwargs:
            self._render_source()
        return self

    def _render_source(self):
        self._first_state_icon.size = self.collider.size
        self._second_state_icon.size = self.collider.size

        self._first_state_filled.surface = self._first_state_icon.surfconst.copy()
        self._first_state_filled.fill(Color.White.rgb, 100)
        self._second_state_filled.surface = self._second_state_icon.surfconst.copy()
        self._second_state_filled.fill(Color.White.rgb, 100)

    def update(self):
        self.minput.update()
        if not self.entity.virtual_visible:
            self.minput.reset()
            self.state = False
            return

        __sprite = self._second_state_icon if self.state else self._first_state_icon
        __sprite.update()
        if not self.entity.virtual_enable:
            self.minput.reset()
            self.state = False
            return

        if self.minput.startedin_left:
            self.state = ~self.state

        if self.minput.hovered:
            __sprite_filled = self._second_state_filled if self.state else self._first_state_filled
            __sprite_filled.update()
