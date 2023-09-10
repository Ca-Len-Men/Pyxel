from pyxelclec.geo.imagine import *
from pyxelclec.model.components.ccollider import CRect
from pyxelclec.model.components.cscript import ComponentScript
from pyxelclec.model.components.csprite import CSprite, CLabel
from pyxelclec.model.base import app

class TimeCounter(ComponentScript):
    def __init__(self, entity, internal):
        super().__init__(entity)
        self._internal = internal
        self._current = 0
        self.tick = False

    def reset(self):
        self._current = self._internal
        self.tick = False

    def update(self):
        self._current += app.time.delta_time
        if self._current >= self._internal:
            self._current -= self._internal
            self.tick = True
        else:
            self.tick = False

class FPSDisplay(ComponentScript):
    def __init__(self, entity, **kwargs):
        self._label = CLabel(text='FPS : 60', color=Color.Chocolate, enhance_opacity=3)
        self._rounded = CSprite()
        self._time_counter = TimeCounter(entity, 1)
        self._collider = CRect(0, 0)
        self._keys_border_radius = {'border': 8}

        entity.add_components(self._collider, self._label, self._rounded)
        entity.re_structured()
        super().__init__(entity)

        self.set(**kwargs)

    def _render_source(self):
        __CONSTANT_PADDING = self._label.w * .3
        __size = self._label.size + Vector(__CONSTANT_PADDING, __CONSTANT_PADDING)

        self._collider.size = __size
        self._rounded.surface = rect_width(__size, self._label.color, 2,
                                                          **self._keys_border_radius)
        self._label.center = self._collider.center

    def set(self, **kwargs):
        if not kwargs:
            return

        self._label.set(**kwargs)

        __keys = keys_border_radius.intersection(kwargs)
        if __keys:
            self._keys_border_radius.clear()
            for key in __keys:
                self._keys_border_radius[key] = kwargs[key]

        self._render_source()

    def update(self):
        if self._time_counter.tick:
            latest_fps = f'FPS : {int(app.time.fps)}'
            if latest_fps != self._label.text:
                self._label.text = latest_fps

        self._label.update()
        self._rounded.update()

    @property
    def collider(self):
        return self._collider