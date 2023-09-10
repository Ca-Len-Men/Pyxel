#cython: language_level=3

from ...geo.color import Color

import pygame.mask

class ComponentCollider(Component, Rect):
    def __init__(self, width, height):
        Component.__init__(self)
        Rect.__init__(self, Vector(width, height))
        self.visible = False

    def update(self):
        if self.visible:
            pygame.draw.rect(
                self.entity.canvas.sprite.surfconst,
                Color.White, (*self.topleft, *self.size), width=1
            )

    @classmethod
    def get_comp(cls):
        return ComponentCollider

class CRect(ComponentCollider):
    pass

class CCircle(ComponentCollider):
    def __init__(self, diameter):
        super().__init__(diameter, diameter)

    def update(self):
        if self.visible:
            pygame.draw.circle(
                self.entity.canvas.sprite.surfconst,
                Color.White, center=self.center, radius=self.w // 2, width=1
            )

    def collide_point(self, Vector point):
        cdef:
            Vector __center = <Vector>self.center
            Rect __self = <Rect>self

        return __center.cy_magnitude(point) <= __self.cy_get_w() / 2