from pyxelclec.geo.fvector import Vector, WeakrefMethod
from pyxelclec.geo.frect import Rect, StructRect
from pyxelclec.model.entity import Entity
from pyxelclec.model.components.csprite import CSprite

import pygame

class CCanvas(CSprite):
    def __init__(self, source, canvas):
        super().__init__(source)
        self._CONSTANT_SOURCE = CSprite(source.copy())
        self._source_alphas = pygame.surfarray.array_alpha(source)
        self._canvas = canvas

    def render_source(self):
        # Filling alphas
        source_alphas = pygame.surfarray.pixels_alpha(self.surface)
        source_alphas[:] = self._source_alphas
        del source_alphas

    def update(self):
        self._canvas.canvas.sprite.blit_sprite(self)
        self.copy_source(self._CONSTANT_SOURCE)

    def blit_sprite(self, sprite):
        self.surface.blit(sprite.surfconst, sprite.topleft)

    def blit_surf(self, surface, position_type):
        if isinstance(position_type, str):
            surface_rect = StructRect(Vector(*surface.get_size()))
            self_rect = StructRect(self.size)
            setattr(surface_rect, position_type, getattr(self_rect, position_type))
            topleft = surface_rect.topleft
        elif isinstance(position_type, tuple):
            surface_rect = StructRect(Vector(*surface.get_size()))
            setattr(surface_rect, position_type[0], position_type[1])
            topleft = surface_rect.topleft
        elif isinstance(position_type, Vector):
            topleft = position_type
        else:
            raise TypeError(f"From {self.__class__.__name__}.blit_surf : "
                            f"parameter type of 'position_type' must be <str, Vector, Tuple[str, Vector]> !")

        self.surface.blit(surface, topleft)

# Khi thay đổi hành vi ( visible, enable ) của một Canvas,
# một lệnh đệ quy tìm qua tất cả các Canvas, Entity có trong `root` để gán lại các `virtual_xxx`
update_behaviour = [False]

class Canvas(Rect):
    def __init__(self, source):
        self.automate = False
        self.__visible = True
        self.__enable = True
        self.virtual_visible = True
        self.virtual_enable = True
        self.alive = True
        self._canvas = None
        self._mouse_position = Vector(0, 0)

        self._entities = set()
        self._canvases = set()
        self._remove_set = set()

        if source is None:

            self._sprite = None
            super().__init__(Vector.zero())
        else:
            self._sprite = CCanvas(source, self)
            super().__init__(Vector(*source.get_size()))
            self.pos_listener(WeakrefMethod(self.__move_listener))

    def __move_listener(self, topleft):
        self._sprite.topleft = topleft

    def init(self):
        source = pygame.display.get_surface()
        self._sprite = CCanvas(source, self)
        self.size = Vector(*source.get_size())

    def update(self):
        # Calling update canvases
        for canvas in self._canvases:
            if canvas.automate:
                canvas.update()
            if not canvas.alive:
                self._remove_set.add(canvas)

        # Calling update entities
        for entity in self._entities:
            if entity.automate:
                # Run scripts of entity
                entity.update()

            if not entity.alive:
                self._remove_set.add(entity)

        self._entities -= self._remove_set
        self._canvases -= self._remove_set
        self._remove_set.clear()

        # Không phải root -> vẽ CCanvas
        if self._canvas is not None:
            if self.virtual_visible:
                self._sprite.render_source()
                self._render()

    def _render(self):
        self.sprite.update()

    def add_entity(self, entity):
        if entity not in self._entities:
            self._entities.add(entity)
            entity.canvas = self

    def add_entities(self, *entities):
        for entity in entities:
            self.add_entity(entity)

    def del_entity(self, entity):
        if entity in self._entities:
            self._entities.discard(entity)
            entity.canvas = None

    def add_canvas(self, canvas):
        if canvas not in self._canvases:
            self._canvases.add(canvas)
            canvas.canvas = self

    def add_canvases(self, *canvases):
        for canvas in canvases:
            self.add_canvas(canvas)

    def del_canvas(self, canvas):
        if canvas in self._canvases:
            self._canvases.discard(canvas)
            canvas.canvas = None

    def update_mouse_position(self):
        if self._canvas:
            self._mouse_position = self._canvas.mpos - self.topleft
        else:
            self._mouse_position.set(pygame.mouse.get_pos())
        for canvas in self._canvases:
            canvas.update_mouse_position()

    def update_virtual_behaviour(self):
        # Nếu nó không phải `root`
        if __parent := self._canvas:
            self.virtual_visible = self.visible and __parent.virtual_visible
            self.virtual_enable = self.enable and __parent.virtual_enable

        for entity in self._entities:
            entity.virtual_visible = entity.visible and self.virtual_visible
            entity.virtual_enable = entity.enable and self.virtual_enable

        # Đệ quy
        for canvas in self._canvases:
            canvas.update_virtual_behaviour()

    @property
    def mpos(self):
        return self._mouse_position

    @property
    def sprite(self):
        return self._sprite

    @property
    def canvas(self):
        return self._canvas

    @canvas.setter
    def canvas(self, __canvas):
        if self._canvas:
            return

        if self in __canvas:
            self._canvas = __canvas

    @property
    def entities(self):
        return self._entities.__iter__()

    @entities.deleter
    def entities(self):
        self._entities.clear()

    @property
    def canvases(self):
        return self._canvases.__iter__()

    @canvases.deleter
    def canvases(self):
        self._canvases.clear()

    @property
    def visible(self):
        return self.__visible

    @visible.setter
    def visible(self, __visible):
        self.__visible = __visible
        update_behaviour[0] = True

    @property
    def enable(self):
        return self.__enable

    @enable.setter
    def enable(self, __enable):
        self.__enable = __enable
        update_behaviour[0] = True

    def __contains__(self, item):
        if isinstance(item, Entity):
            return item in self._entities
        elif isinstance(item, Canvas):
            return item in self._canvases
        else:
            raise TypeError(f"From {self.__class__.__name__}.__contains__ : "
                            f"parameter type of `item` must be <Entity, Canvas> !")

root = Canvas(None)
