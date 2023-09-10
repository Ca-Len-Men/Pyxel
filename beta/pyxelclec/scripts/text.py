from pyxelclec.__flag__ import FLAG_NO_RENDER
from pyxelclec.geo.fvector import WeakrefMethod
from pyxelclec.geo.imagine import *

from pyxelclec.model.entity import Entity
from pyxelclec.model.components.cinput import CMouseInput, CKeyInput, KEY_INPUT, BACKSPACE
from pyxelclec.model.components.ccollider import CCircle
from pyxelclec.model.components.cscript import ComponentScript
from pyxelclec.model.components.csprite import CSprite, CLabel, CMask
from pyxelclec.asset import image_cache
from pyxelclec.scripts.button import ButtonState

from abc import ABC

class TextScript(ComponentScript, ABC):
    def __init__(self, entity):
        super().__init__(entity)
        self._background = CSprite()
        self._collider = CMask()
        self._mouse_input = CMouseInput()
        self._key_input = CKeyInput()
        entity.add_components(self._collider, self._mouse_input,
                              self._key_input, self._background)

    @property
    def collider(self):
        return self._collider

class TextField(TextScript):
    __keys = {'validator', 'width', 'size', 'text'}
    keys = __keys | CLabel.keys | keys_border_radius | {'placeholder'}

    def __init__(self, entity, **kwargs):
        super().__init__(entity)
        self._keys_border_radius = {'border': FULL_BORDER_RADIUS}
        self._width = 2
        self._text = ''
        self._size = None
        self._validator = None
        self._focus = False

        self._label = CLabel(text='', color=Color.Dark, enhance_opacity=2)
        self._place_holder = CLabel(text='Input your string', color=Color.Gray, enhance_opacity=2)
        self._border_focus = CSprite()

        entity.add_components(self._label, self._place_holder, self._border_focus)
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

        # Kiểu tra khóa 'font_size', 'font_name', 'placeholder' -> thay đổi placeholder
        __special_keys = {'font_size', 'font_name', 'placeholder'}
        __keys = __special_keys.intersection(kwargs)
        if __keys:
            __new_kwargs = {key: kwargs[key] for key in __keys}

            # Khóa 'placeholder' chỉ thị cho 'text' của label place_holder -> xử lí riêng
            __placeholder_text = __new_kwargs.get('placeholder')
            if __placeholder_text:
                # Đổi từ 'placeholder' sang 'text'
                del __new_kwargs['placeholder']
                __new_kwargs['text'] = __placeholder_text
            self._place_holder.set(**__new_kwargs)

        self._label.set(**kwargs)

        __keys = keys_border_radius.intersection(kwargs)
        if __keys:
            self._keys_border_radius.clear()
            for key in __keys:
                self._keys_border_radius[key] = kwargs[key]

        __keys = TextField.__keys.intersection(kwargs)
        if __keys:
            for key in __keys:
                setattr(self, f'_{key}', kwargs[key])

        if not __flag_no_render:
            self._render_source()
        return self

    def _render_source(self):
        size = self._size
        if size is None:
            __CONSTANT_PADDING = self._place_holder.h
            size = self._place_holder.size + Vector(__CONSTANT_PADDING, __CONSTANT_PADDING)
            size.x += size.y / 2
        self.collider.size = size

        self._background.surface = rect(size, Color.White, **self._keys_border_radius)
        self._border_focus.surface = rect_width(size, Color.Dark, self._width,
                                                               **self._keys_border_radius)

        self._place_holder.midleft = self.collider.midleft + Vector(size.y / 2, 0)
        self._label.midleft = self._place_holder.midleft

    def update(self):
        self._mouse_input.update()
        self._key_input.update()

        if not self.entity.virtual_visible:
            self._mouse_input.reset()
            self._key_input.reset()
            return

        # Render
        self._background.update()
        if self._focus:
            self._border_focus.update()
        if len(self._label.text) == 0:
            self._place_holder.update()
        else:
            self._label.update()

        if not self.entity.virtual_enable:
            self._mouse_input.reset()
            self._key_input.reset()
            self._focus = False
            return

        if self._mouse_input.started_left:
            self._focus = self._mouse_input.startedin_left

        # Check char from key board input
        if self._focus and self._key_input.state == KEY_INPUT:
            text_string = self._text
            char = self._key_input.char

            if char == BACKSPACE:
                if len(text_string) != 0:
                    text_string = text_string[:-1]
            else:
                text_string += self._key_input.char

            # Text is valid
            if self._validator is None or self._validator(text_string, char):
                self._add_char_input(text_string, char)
                self._label.midleft = self.collider.midleft + Vector(self.collider.h / 2, 0)

    def _add_char_input(self, __string, __char):
        self._text = __string
        self._label.text = self._text
        self._label.midleft = self._place_holder.midleft

class TextPassword(TextField):
    def __init__(self, entity, **kwargs):
        self._btn_show_pass = ButtonState(Entity(),
                                          image_cache.load('show.png'),
                                          image_cache.load('hide.png'),
                                          collider=CCircle(256))

        super().__init__(entity, **kwargs)
        if 'placeholder' not in kwargs:
            self._place_holder.text = 'Input password'
            self._place_holder.midleft = self._label.midleft
        self.collider.pos_listener(WeakrefMethod(self.__move_listener))

    def __move_listener(self, topleft):
        self._btn_show_pass.collider.midright = self.collider.midright - Vector(self.collider.h / 2, 0)

    def entity_to_canvas(self, canvas):
        canvas.add_entity(self._btn_show_pass.entity)

    def _render_source(self):
        __CONSTANT_PADDING = self._place_holder.h
        __CONSTANT_BUTTON_SIZE = __CONSTANT_PADDING * 1.2
        if self._size is None:
            size = self._place_holder.size + Vector(__CONSTANT_PADDING + __CONSTANT_BUTTON_SIZE,
                                                    __CONSTANT_PADDING)
            size.x += size.y / 2
            self._area = size

        super()._render_source()
        self._btn_show_pass.set(size=Vector(__CONSTANT_BUTTON_SIZE, __CONSTANT_BUTTON_SIZE))
        self._btn_show_pass.collider.midright = self.collider.midright - Vector(self.collider.h / 2, 0)

    def _add_char_input(self, string, __char):
        self._text = string
        if self._btn_show_pass.state:   # Show password
            self._label.text = self._text
        else:
            self._label.text = '*' * len(self._text)

    def update(self):
        super().update()
        self._btn_show_pass.update()

        if not self.entity.virtual_enable:
            return

        # Clicked button
        if self._btn_show_pass.minput.startedin_left:
            if self._btn_show_pass.state:   # Show password
                self._label.text = self._text
            else:
                self._label.text = '*' * len(self._text)
            self._label.midleft = self._place_holder.midleft
