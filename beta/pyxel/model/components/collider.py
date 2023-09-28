# /**************************************************************************/
# /*  collider.py                                                           */
# /**************************************************************************/
# /*                         This file is part of:                          */
# /*                                 PYXEL                                  */
# /*                  https://github.com/Ca-Len-Men/Pyxel                   */
# /**************************************************************************/


from pyxel.model.component import Component
from pyxel.struct.prect import Rect
from pyxel.struct.pvector import Vector, VectorDependent
from pyxel.struct.pcolor import White

import pygame

class ComponentCollider(Component):
    def __init__(self, size: Vector):
        Component.__init__(self)
        self.__rect = Rect(size, VectorDependent(0, 0))
        self.visible = False

    def research(self, entity) -> None:
        self.rect.get_position().set_ref(entity.rect.get_position())

    def _draw(self):
        pygame.draw.rect(
            self.entity.canvas.sprite.surfconst,
            White, tuple(self.rect), width=1
        )

    def update(self):
        if not self.visible:
            return

        if self.rect.size == Vector(0, 0):
            pygame.draw.circle(self.entity.canvas.sprite.surfconst,
                               White, self.rect.topleft, 2)
        else:
            self._draw()

    def collide_point(self, point: Vector):
        return self.rect.collide_point(point)

    @property
    def rect(self):
        return self.__rect

    def __hash__(self):
        return id(ComponentCollider)

class CRect(ComponentCollider):
    pass

class CCircle(ComponentCollider):
    def __init__(self, diameter):
        super().__init__(Vector(diameter, diameter))

    def _draw(self):
        pygame.draw.circle(
            self.entity.canvas.sprite.surfconst,
            White, center=self.rect.center, radius=self.rect.w // 2, width=1
        )

    def collide_point(self, point: Vector):
        return self.rect.center.magnitude(point) <= (self.rect.w / 2)
