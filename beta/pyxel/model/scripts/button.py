# /**************************************************************************/
# /*  button.py                                                             */
# /**************************************************************************/
# /*                         This file is part of:                          */
# /*                                 PYXEL                                  */
# /*                  https://github.com/Ca-Len-Men/Pyxel                   */
# /**************************************************************************/

from pyxel.info import FLAG_NO_RENDER
from pyxel.struct.processor_surface import *
from pyxel.model.entity import Entity
from pyxel.model.components.collider import CRect
from pyxel.model.components.sprite import CSprite, CMask, CLabel
from pyxel.model.scripts.control import ButtonNormal

import pygame
from typing import *

class ButtonIcon(ButtonNormal):
    """
    - Chỉ cần một icon là sẽ có thể trở thành một button.
    - Khi hover vào button, phủ lên icon một lớp màu.
    - Kích thước button sẽ thay đổi dựa vào kích thước collider của nó và `entity.rect`.
    """

    keys = {'size'}

    def __init__(self, icon: Union[str, pygame.Surface], *,
                 collider=None, entity=None):
        if entity is None:
            entity = Entity()
        self._icon = CSprite(icon)
        self._icon_filled = CSprite()

        if collider is None:
            collider = CRect(self._icon.rect.size)
        elif isinstance(collider, CMask):
            collider.sprite = self._icon

        entity.rect.get_size().delegate.add(self, ButtonIcon._event_entity_rect_size_changed)
        entity.add_components(self._icon, self._icon_filled)
        super().__init__(collider, entity=entity)
        self._render_source()
        entity.re_structured()

    def _event_entity_rect_size_changed(self, size):
        self._collider.rect.get_size().only_set(size)
        self.entity.rect.get_size().only_set(size)
        self._icon.rect.size = size
        self._icon_filled.surface = self._icon.surfconst.copy()
        self._icon_filled.fill(White.rgb, 100)

    def _render_source(self):
        self._event_entity_rect_size_changed(self._collider.rect.size)

    def _normalized(self):
        self._collider.update()
        self._icon.update()

    def _hovered(self):
        self._collider.update()
        self._icon.update()
        self._icon_filled.update()

    _pressed = _hovered
    _clicked = _hovered

class ButtonState(ButtonNormal):
    keys = {'size'}

    def __init__(self, first_state_icon, second_state_icon, *, collider=None, entity=None):
        if entity is None:
            entity = Entity()
        self.state = False
        self._first_state_icon = CSprite(first_state_icon)
        self._first_state_filled = CSprite()
        self._second_state_icon = CSprite(second_state_icon)
        self._second_state_filled = CSprite()

        if collider is None:
            collider = CRect(self._first_state_icon.rect.size)

        entity.add_components(self._first_state_icon, self._second_state_icon,
                              self._first_state_filled, self._second_state_filled)
        super().__init__(collider, entity=entity)
        entity.re_structured()
        self._render_source()
    
    def _event_entity_rect_size_changed(self, size: Vector):
        self._collider.rect.get_size().only_set(size)
        self.entity.rect.get_size().only_set(size)
        self._first_state_icon.rect.size = size
        self._second_state_icon.rect.size = size

        self._first_state_filled.surface = self._first_state_icon.surfconst.copy()
        self._first_state_filled.fill(White.rgb, 100)
        self._second_state_filled.surface = self._second_state_icon.surfconst.copy()
        self._second_state_filled.fill(White.rgb, 100)

    def set(self, **kwargs):
        if not kwargs:
            self._render_source()
            return

        __value = kwargs.get('size')
        if __value:
            self._collider.rect.size = __value

        if FLAG_NO_RENDER not in kwargs:
            self._render_source()
        return self

    def _render_source(self):
        self._event_entity_rect_size_changed(self._collider.rect.size)

    def _normalized(self):
        __sprite = self._second_state_icon if self.state else self._first_state_icon
        __sprite.update()

    def _hovered(self):
        self._normalized()
        __sprite_filled = self._second_state_filled if self.state else self._first_state_filled
        __sprite_filled.update()

    def _clicked(self):
        self._hovered()
        self.state = ~self.state

    _pressed = _hovered

class ButtonBootstrap(ButtonNormal):
    _keys = {'width', 'size'}
    keys = _keys | CLabel.keys | keys_border_radius

    def __init__(self, *, entity=None, **kwargs):
        if entity is None:
            entity = Entity()

        self._keys_border_radius = {'border': 8}
        self._width = 2
        self._size = None
        self._label = CLabel(enhance_opacity=2)
        self._first_sprite = CSprite()
        self._second_sprite = CSprite()

        super().__init__(CRect(Vector(0, 0)), entity=entity)
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
        # Chỉ định kích thước
        size = self._size
        # Tự tính kích thước dựa vào label
        if size is None:
            __CONSTANT_PADDING = self._label.rect.h
            size = self._label.rect.size + Vector(__CONSTANT_PADDING, __CONSTANT_PADDING)

        first_rounded = new_rect_width(size, self._label.color, self._width,
                                                  **self._keys_border_radius)
        second_rounded = new_rect(size, self._label.color,
                                             **self._keys_border_radius)

        self._first_sprite.surface = new_surface(size)
        self._second_sprite.surface = new_surface(size)

        self._first_sprite.blit(first_rounded, (0, 0))
        self._first_sprite.blit(self._label.surfconst, 'center')
        self._second_sprite.blit(second_rounded, (0, 0))
        self._second_sprite.sub(self._label, 'center')

        self._collider.rect.size = size
        self.entity.rect.size = size

    def _normalized(self):
        self._first_sprite.update()

    def _hovered(self):
        self._second_sprite.update()

    _pressed = _hovered
    _clicked = _hovered
