__doc__ = '''           Ngày tạo : 24/11/2022
File Control.py     : định nghĩa các lớp điều khiển trong trò chơi ( button, textbox, checkbox, table, ... ).
'''

import pygame
import inspect
import functools
from abc import ABC, abstractmethod
from typing import Union, Callable, Tuple, List, Dict, Any
from speedgame.Surface import ImageProcessor, Image, Label
from speedgame.Basic import Color, Vector2, font, Font, Resource
from speedgame.Handle import app


__version__ = '1.0.0'


class CheckParams:
    """Lớp **CheckParams** : kiểm tra sự hợp lệ của các tham số đầu vào của một hàm."""

    __doc__ = '''Lớp CheckParams : lưu danh sách các inspect.Parameter.
                nó kiểm tra một hàm có các tham số hợp lệ ( gần giống ) với danh sách các inspect.Parameter.'''

    def __init__(
        self,
        list_param: List[inspect.Parameter],
        cmp_predicate: Dict[str, range]
    ):
        """ Khởi tạo **CheckParams** : nhận vào *List inspect.Parameter* và *dict* cho biết cần so sánh những gì.

        :param list_param: danh sách các inspect.Parameter.
        :param cmp_predicate: một dictionary gồm các cặp (name_attrib, range).
        """

        self.list_param = list_param
        self.cmp_predicate = cmp_predicate

    def __call__(self, callable_object):
        """ Phương thức **__call__** : kiểm tra các tham số của *callable object*.

        :param callable_object: một callable object cần kiểm tra.
        :return: Trả về True nếu tất cả giá trị so sánh đều là True.
        """

        assert callable(callable_object), f'Tham số "function" không phải là một callable object !'

        params = list(inspect.signature(callable_object).parameters.values())
        for name_attrib, indexes in self.cmp_predicate.items():
            for i in indexes:
                assert getattr(params[i], name_attrib) == getattr(self.list_param[i], name_attrib), \
                    f'Giá trị {params[i]}.{name_attrib} không hợp lệ !'


class Control(ABC):
    """Lớp **Control** : lớp tổng quát cho các lớp điều khiển, tương tác qua màn hình."""

    __doc__ = 'Lớp Control : lớp tổng quát cho các lớp điều khiển, tương tác qua màn hình.'

    # def event_click(self, **kwargs): pass
    check_event_click = CheckParams([inspect.Parameter('self', inspect.Parameter.POSITIONAL_OR_KEYWORD),
                                     inspect.Parameter('kwargs', inspect.Parameter.VAR_KEYWORD)],
                                    {'name': range(2), 'kind': range(2)})

    # def event_hover(self, **kwargs): pass
    check_event_hover = CheckParams([inspect.Parameter('self', inspect.Parameter.POSITIONAL_OR_KEYWORD),
                                     inspect.Parameter('kwargs', inspect.Parameter.VAR_KEYWORD)],
                                    {'name': range(2), 'kind': range(2)})

    class CallEvent:
        """Lớp **CallEvent** : lưu trữ các đối tượng control, và các hàm sự kiện."""

        __doc__ = 'Lớp CallEvent : lưu trữ các đối tượng control, và các hàm sự kiện.'

        def __init__(
            self,
            control,
            event: Callable[..., None]
        ):
            """ Khởi tạo **CallEvent** : một *callable object* được xem như một sự kiện trên *control*.

            :param control: một control bất kỳ ( button, textbox, ... ).
            :param event: một hàm sự kiện bất kỳ ( phải là function ).
            """

            self.control = control
            self.event = event

        def __call__(self, *args, **kwargs):
            """ Phương thức **__call__** : gọi một sự kiện.

            :param args: các tham số là POSITIONAL_OR_KEYWORD từ đối tượng control truyền vào.
            :param kwargs: các tham số là KEYWORD_ONLY từ đối tượng control truyền vào.
            """

            self.event(self.control, *args, **kwargs)

    def __init__(self, position: Union[Vector2, Tuple[int, int]]):
        if type(position) is tuple:
            self._position = Vector2(*position)
        else:
            self._position = position

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, new_position: Union[Vector2, Tuple[int, int]]):
        if type(new_position) is tuple:
            self._position = Vector2(*new_position)
        else:
            self._position = new_position

    @classmethod
    def check_event(
        cls,
        event_name: str,
        event_callable: Union[Callable[..., Any], functools.partial]
    ):
        """ Phương thức **check_event** : kiểm tra một hàm sự kiện.

        :param event_name: Tên sự kiện.
        :param event_callable: Hàm sự kiện.
        :return: None.
        """

        check_params = getattr(cls, 'check_' + event_name)
        if isinstance(event_callable, functools.partial):
            check_params(event_callable.func)
        else:
            check_params(event_callable)

    @abstractmethod
    def update(self, action=True): pass


class Button(Control):
    """Class **Button** : lớp tổng quát cho các *button*."""

    __doc__ = 'Lớp Button : dạng chung của một button cho các lớp Button khác kế thừa.'

    def __init__(self, position: Union[Vector2, Tuple[int, int]]):
        super().__init__(position)
        self.click = self.multi_click = False
        self.hover = False
        self._e_click = None
        self._e_hover = None

    @property
    def e_click(self):
        """ Property **e_click** getter : xem sự kiện nhấp chuột trái.

        :return: Optional[None, Control.CallEvent]
        """

        return self._e_click

    @e_click.setter
    def e_click(self, event_click: Callable[..., None]):
        """ Property **e_click** setter : gán một hàm cho sự kiện nhấp chuột trái.

        * Định dạng hàm sự kiện **click** : def [*function_name*] (*self*, ***kwargs*)

        :param event_click: Một hàm sự kiện.
        """

        Control.check_event('event_click', event_click)
        self._e_click = Control.CallEvent(self, event_click)

    @property
    def e_hover(self):
        """ Property **e_hover** getter : xem sự kiện di chuột lên *button*.

        :return: Optional[None, Control.CallEvent]
        """

        return self._e_hover

    @e_hover.setter
    def e_hover(self, event_hover: Callable[..., None]):
        """ Property **e_hover** setter : gán một hàm cho sự di chuột lên *button*.

        * Định dạng hàm sự kiện **hover** : def [*function_name*] (*self*, ***kwargs*)


        :param event_hover: một hàm sự kiện.
        """

        Control.check_event('event_hover', event_hover)
        self._e_hover = Control.CallEvent(self, event_hover)

    @abstractmethod
    def collide_point(self, point: Union[Vector2, Tuple[int, int]]) -> bool: pass

    def update(self, action=True):
        if not action:
            self.hover = self.click = self.multi_click = False
            return

        self.hover = self.collide_point(app.cursor.position)
        self.click = app.cursor.left and self.hover
        self.multi_click = app.cursor.multi_left and self.hover

        if self.hover and self._e_hover:
            self._e_hover()
        if self.click and self._e_click:
            self._e_click()


class ButtonBoostrap(Button):
    """Class **ButtonBoostrap** : mô phỏng theo *button* của *Boostrap*."""

    __doc__ = 'Lớp ButtonBoostrap : mô phỏng theo Button của Bootstrap.'

    def __init__(
        self,
        position: Union[Vector2, Tuple[int, int]],
        text: str = 'Button',
        font_size: int = 20,
        bg_color=Color.Chocolate,
        text_color=Color.Chocolate,
        style=Label.STYLE_DEFAULT,
        border_radius=8,
        font_name=Resource.font_name
    ):
        super().__init__(position)
        self._src_font: Font = font[font_name]      # Font chữ
        self._text = text                           # Văn bản
        self._font_size = font_size                 # Kích cỡ chữ
        self._text_color = text_color               # Màu chữ
        self._bg_color = bg_color                   # Màu nền
        self._style = style                         # Kiểu chữ
        self._border_radius = border_radius         # Bo góc
        self._fg_surface: pygame.Surface            # Ảnh chữ, có viền
        self._bg_surface: pygame.Surface            # Ảnh nền, chữ rỗng

        self.__change_surface()

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, new_position: Union[Vector2, Tuple[int, int]]):
        Control.position.fset(self, new_position)
        self._fg_surface.rect.center = new_position
        self._bg_surface.rect.center = new_position

    def __change_surface(self):
        size_text = self._src_font.get_rect(self._text, self._style, size=self._font_size).size
        padding = size_text[1]

        fg_label = self._src_font.render(self._text, self._text_color, style=self._style, size=self._font_size)[0]
        bg_label = self._src_font.render(self._text, bgcolor=self._bg_color, style=self._style, size=self._font_size)[0]
        image_fg = ImageProcessor.surface_padding(fg_label, padding)
        image_fg = ImageProcessor.rect(image_fg, self._bg_color, 1, self._border_radius)
        image_bg = ImageProcessor.surface_padding(bg_label, padding)
        image_bg = ImageProcessor.rect(image_bg, self._bg_color, border_radius=self._border_radius)

        self._fg_surface = Image(image_fg, self._position)
        self._bg_surface = Image(image_bg, self._position)

    def collide_point(self, point: Union[Vector2, Tuple[int, int]]):
        """ Phương thức **collide_point** : kiểm tra một điểm nằm trên *button*.

        :param point: Một điểm trong mặt phẳng.
        :return: Trả về True nếu điểm đó nằm trên button.
        """

        return self._fg_surface.collide_point(point)

    def update(self, action=True):
        """ Phương thức **action** : cập nhật *button* trên màn hình.

        :param action: True nếu muốn button hoạt động.
        :return: None
        """

        super().update(action)
        if action and self.hover:
            self._bg_surface.update(action)
        else:
            self._fg_surface.update(action)


class ButtonImage(Button):
    """Class **ButtonImage** : tạo hiệu ứng nhấp chuột trên hình ảnh *button*."""

    __doc__ = 'Lớp ButtonImage : bắt sự kiện nhấp chuột vào button, lưu hình ảnh button'

    def __init__(
        self,
        button_image: pygame.Surface,
        position: Union[Vector2, Tuple[int, int]],
        fill_color: Tuple[int, int, int, int]
    ):
        super().__init__(position)
        self._image = Image(button_image, position)
        self._mask = pygame.mask.from_surface(button_image)
        self._fill_image = Image(ImageProcessor.fill_mask(button_image, fill_color, self._mask), position)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, new_position: Union[Vector2, Tuple[int, int]]):
        Control.position.fset(self, new_position)
        self._image.rect.center = new_position
        self._fill_image.rect.center = new_position

    def collide_point(self, point: Union[Vector2, Tuple[int, int]]):
        """ Phương thức **collide_point** : kiểm tra một điểm nằm trên ảnh của *button*.

        :param point: Một điểm trong mặt phẳng.
        :return: Trả về True nếu điểm đó nằm trên button.
        """

        left_top = self._image.rect.topleft

        x = int(point[0] - left_top[0])
        if x < 0 or x >= self._image.width:
            return False
        y = int(point[1] - left_top[1])
        if y < 0 or y >= self._image.height:
            return False
        return bool(self._mask.get_at((x, y)))

    def update(self, action=True):
        """ Phương thức **action** : cập nhật *button* trên màn hình.

        :param action: True nếu muốn button hoạt động.
        :return: None
        """

        super().update(action)
        if action and self.hover:
            self._fill_image.update(action)
        else:
            self._image.update(action)
