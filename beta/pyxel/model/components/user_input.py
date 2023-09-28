# /**************************************************************************/
# /*  user_input.py                                                         */
# /**************************************************************************/
# /*                         This file is part of:                          */
# /*                                 PYXEL                                  */
# /*                  https://github.com/Ca-Len-Men/Pyxel                   */
# /**************************************************************************/

from pyxel.struct.pvector import Vector
from pyxel.model.component import Component, ONLY_ONE
from pyxel.model.components.collider import ComponentCollider
from pyxel.model.base import app

import pygame

class ComponentMouseInput(Component):
    def __init__(self):
        super().__init__()
        self.__collider = None
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

    def set_collider(self, __collider: ComponentCollider):
        self.__collider = __collider

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

    def __updating_pressedin(self):
        self.hovered = self.__collider.collide_point(self.mpos)
        self.startedin_left = self.startedin_right = False
        self.endedin_left = self.endedin_right = False

        # Left pressed in
        if self.pressed_left:
            if self.hovered and self.started_left:  # First pressed in area
                self.startedin_left = True
                self.__touch_pos.set(self.mpos)
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

    def __updating_dragged(self):
        self.drag_started = self.drag_ended = False

        if self.dragging:
            if self.endedin_left:
                self.dragging = False
                self.drag_ended = True
        else:
            if self.pressedin_left and self.__touch_pos != self.mpos:
                self.drag_started = self.dragging = True

    def update(self):
        self.__updating_pressed()
        self.__updating_pressedin()
        self.__updating_dragged()

    @property
    def dragged_vector(self):
        return self.mpos - self.__touch_pos

    @property
    def mpos(self):
        return self.entity.canvas.mpos

    def quantity(self) -> int:
        return ONLY_ONE

    def __hash__(self):
        return id(ComponentMouseInput)

class CMouseInput(ComponentMouseInput):
    pass

KEY_INPUT = 0b001
NO_KEY_INPUT = 0b010
BACKSPACE = '\x08'

class ComponentKeyInput(Component):
    def __init__(self):
        super().__init__()
        self.state = NO_KEY_INPUT
        self.char = '\0'

    def reset(self):
        self.state = NO_KEY_INPUT
        self.char = '\0'

    def update(self):
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

    def quantity(self) -> int:
        return ONLY_ONE

    def __hash__(self):
        return id(ComponentKeyInput)

class CKeyInput(ComponentKeyInput):
    pass

