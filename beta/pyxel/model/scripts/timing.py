# /**************************************************************************/
# /*  timing.py                                                             */
# /**************************************************************************/
# /*                         This file is part of:                          */
# /*                                 PYXEL                                  */
# /*                  https://github.com/Ca-Len-Men/Pyxel                   */
# /**************************************************************************/

from pyxel.struct.processor_surface import *
from pyxel.model.components.script import ComponentScript
from pyxel.model.components.sprite import CSprite, CLabel
from pyxel.model.entity import Entity
from pyxel.model.base import app

class TimeInterval(ComponentScript):
    def __init__(self, entity, second_internal):
        super().__init__(entity)
        self._second_internal = second_internal
        self._current = 0
        self.tick = False

    def reset(self):
        self._current = self._second_internal
        self.tick = False

    def update(self):
        self._current += app.time.delta_time
        if self._current >= self._second_internal:
            self._current -= self._second_internal
            self.tick = True
        else:
            self.tick = False

class FPSDisplay(ComponentScript):
    def __init__(self, *, entity=None, **kwargs):
        if entity is None:
            entity = Entity()
        self._label = CLabel(text='FPS : 60', color=Chocolate, enhance_opacity=2)
        self._sprite_rounded = CSprite()
        self._time_interval = TimeInterval(entity, 1)
        self._keys_border_radius = {'border': 8}

        entity.add_components(self._label, self._sprite_rounded)
        entity.re_structured()
        super().__init__(entity)

        self.set(**kwargs)

    def _render_source(self):
        __CONSTANT_PADDING = self._label.rect.w * .3
        __size = self._label.rect.size + Vector(__CONSTANT_PADDING, __CONSTANT_PADDING)

        self.entity.rect.size = __size
        self._sprite_rounded.surface = new_rect_width(__size, self._label.color, 2,
                                                      **self._keys_border_radius)
        self._label.rect.center = self.entity.rect.center

    def set(self, **kwargs):
        if not kwargs:
            if not self._sprite_rounded.has_surface:
                self._render_source()
            return

        self._label.set(**kwargs)

        __keys = keys_border_radius.intersection(kwargs)
        if __keys:
            self._keys_border_radius.clear()
            for key in __keys:
                self._keys_border_radius[key] = kwargs[key]

        self._render_source()

    def update(self):
        if self._time_interval.tick:
            latest_fps = f'FPS : {int(app.time.fps)}'
            if latest_fps != self._label.text:
                self._label.text = latest_fps

        self._label.update()
        self._sprite_rounded.update()
