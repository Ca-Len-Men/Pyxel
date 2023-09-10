#cython: language_level=3

from .ccollider import ComponentCollider
from ..base import app
import pygame

cdef class ComponentMouseInput(Component):
    #TODO     =====     Cython     =====

    cdef void __cy_updating_pressed(self):
        cdef:
            bint left, _, right

        left, _, right = pygame.mouse.get_pressed(num_buttons=3)
        self.started_left = self.started_right = False
        self.ended_left = self.ended_right = False

        if left:
            if not self.pressed_left:
                self.started_left = True
        else:
            if self.pressed_left:
                self.ended_left = True

        if right:
            if not self.pressed_right:
                self.started_right = True
        else:
            if self.pressed_right:
                self.ended_right = True

        self.pressed_left, self.pressed_right = left, right

    cdef void __cy_updating_pressedin(self):
        self.hovered = self.__area.collide_point(self.cy_get_mpos())
        self.startedin_left = self.startedin_right = False
        self.endedin_left = self.endedin_right = False

        # Left pressed in
        if self.pressed_left:
            if self.hovered and self.started_left:  # First pressed in area
                self.startedin_left = True
                self.__touch_pos.cy_set(self.cy_get_mpos())
                self.pressedin_left = True
        else:  # Release
            if self.pressedin_left:  # First release
                self.endedin_left = True
                self.pressedin_left = False

        # Right pressed in
        if self.pressed_right:
            if self.hovered and self.started_right:  # First pressed in area
                self.startedin_right = True
                self.pressedin_right = True
        else:  # Release
            if self.pressedin_right:  # First release
                self.endedin_right = True
                self.pressedin_right = False

    cdef void __cy_updating_dragged(self):
        self.drag_started = self.drag_ended = False

        if self.dragging:
            if self.endedin_left:
                self.dragging = False
                self.drag_ended = True
        else:
            if self.pressedin_left and self.__touch_pos.cy_neq(self.cy_get_mpos()):
                self.drag_started = self.dragging = True

    cdef void cy_update(self):
        self.__cy_updating_pressed()
        self.__cy_updating_pressedin()
        self.__cy_updating_dragged()

    cdef void cy_research(self, entity):
        self.__area = self.entity.get_component(ComponentCollider)

    cdef Vector cy_get_dragged_vector(self):
        return self.cy_get_mpos().cy_sub(self.__touch_pos)

    cdef Vector cy_get_mpos(self):
        return self.entity.canvas.mpos

    #TODO     =====     Pure Python     =====

    def __init__(self):
        super().__init__()
        self.__area = None
        self.__touch_pos = Vector(0, 0)
        self.hovered = False

        self.pressed_left = False
        self.pressed_right = False
        self.started_left = False
        self.started_right = False
        self.ended_left = False
        self.ended_right = False

        self.pressedin_left = False
        self.pressedin_right = False
        self.startedin_left = False
        self.startedin_right = False
        self.endedin_left = False
        self.endedin_right = False

        self.started_dragging = False
        self.dragging = False
        self.ended_dragging = False

    def reset(self):
        self.hovered = False
        self.state_left = False
        self.state_right = False
        self.pressedin_left = False
        self.pressedin_right = False
        self.clickedin_left = False
        self.clickedin_right = False

        self.drag_started = False
        self.dragging = False
        self.drag_ended = False

    def __updating_pressed(self):
        self.__cy_updating_pressed()

    def __updating_pressedin(self):
        self.__cy_updating_pressedin()

    def __updating_dragged(self):
        self.__cy_updating_dragged()

    def update(self):
        self.cy_update()

    def research(self, entity):
        self.cy_research(entity)

    @property
    def dragged_vector(self):
        return self.mpos - self.__touch_pos

    @property
    def mpos(self):
        return self.entity.canvas.mpos

    @classmethod
    def get_comp(cls):
        return ComponentMouseInput

class CMouseInput(ComponentMouseInput):
    pass

class ComponentKeyInput(Component):
    #TODO     =====     Cython     =====

    cdef void cy_reset(self):
        self.state = NO_KEY_INPUT
        self.char = '\0'

    cdef void cy_update(self):
        self.state = NO_KEY_INPUT

        for event in app.events:
            if event.type != pygame.KEYDOWN:
                continue

            self.state = KEY_INPUT
            # KEY DOWN
            if pygame.key.get_mods() & pygame.KMOD_SHIFT and event.unicode.isalpha():
                self.char = event.unicode.upper()
            else:
                self.char = event.unicode

    #TODO     =====     Pure Python     =====

    def __init__(self):
        super().__init__()
        self.state = NO_KEY_INPUT
        self.char = '\0'

    def reset(self):
        self.cy_reset()

    def update(self):
        self.cy_update()

    @classmethod
    def get_comp(cls):
        return ComponentKeyInput

cdef class CKeyInput(ComponentKeyInput):
    pass
