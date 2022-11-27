__doc__ = '''           Ngày tạo : 18/11/2022
File Surface.py     : định nghĩa các vật lớp trong game ( hình ảnh, đối tượng game).
Lớp ImageProcessor  : cung cấp các phương thức cần thiết để xử lí các hình ảnh trong trò chơi.
Lớp Image           : lưu trữ dữ liệu dạng hình ảnh ( tương tự pygame.Surface ).
Lớp Label           : lưu trữ dữ liệu văn bản dạng hình ảnh, cho phép thay đổi văn bản.
'''

import pygame
from typing import Union, Tuple, List
from abc import ABC, abstractmethod
from speedgame.Handle import app
from speedgame.Basic import Color, Vector2, StaticClassMeta, Resource, Font, font

__version__ = '1.0.0'


class ImageProcessor(metaclass=StaticClassMeta):
    """ Lớp **ImageProcessor** : cung cấp các phương thức cần thiết để xử lí hình ảnh trong game."""

    __doc__ = 'Class ImageProcessor : lớp xử lí hình ảnh trong game.'

    @staticmethod
    def scale(surface: pygame.Surface, new_size: Union[float, Tuple[int, int], Tuple[float, float]]):
        """ Phương thức **scale** : phóng to hoặc thu nhỏ hình ảnh với tỷ lệ hoặc kích thước được cung cấp.\n
        - Nếu **new_size** là *int* hoặc *float* : kích thước mới bằng kích thước cũ nhân với **new_size**.\n
        - Nếu **new_size** là *Tuple[float, float]* :
        kích thước cũ là *(w, h)* và **new_size** là *(per_w, per_h)* -> kích thước mới là *(w * per_w, h * per_h)*.\n
        - Nếu **new_size** là *Tuple[int, int]* : kích thước mới bằng chính **new_size**.

        :param surface: pygame.Surface
        :param new_size: int, float or Tuple[int, int] or Tuple[float, float]
        :return: pygame.Surface
        """

        size = surface.get_size()

        if type(new_size) is int or type(new_size) is float:
            size = (int(size[0] * new_size), int(size[1] * new_size))

            if new_size < 0:
                surface = pygame.transform.flip(surface, True, True)
        elif type(new_size) is tuple:
            flip_x = flip_y = False
            if new_size[0] < 0:
                flip_x = True
            if new_size[1] < 0:
                flip_y = True
            if flip_x or flip_y:
                surface = pygame.transform.flip(surface, flip_x, flip_y)
                new_size = (abs(new_size[0]), abs(new_size[1]))

            if type(new_size[0]) is int:
                size = new_size
            elif type(new_size[0]) is float:
                size = (int(size[0] * new_size[0]), int(size[1] * new_size[1]))

        return pygame.transform.scale(surface, size)

    @staticmethod
    def surface(size: Tuple[int, int], color=Color.NoColor):
        """ Phương thức **surface** : tạo mới một ảnh chữ nhật có màu nền là *color*.

        :param size: Tuple[int, int]
        :param color: Tuple[int, int, int, int]
        :return: pygame.Surface
        """

        surface = pygame.Surface(size, pygame.SRCALPHA)
        surface.fill(color)
        return surface

    @staticmethod
    def surface_padding(
        surface: pygame.Surface,
        padding: Union[int, Tuple[int, int, int, int]],
        color=Color.NoColor
    ):
        """ Phương thức **surface_padding** : tạo một ảnh mới từ *surface* với tham số *padding* nhận vào.

        - Nếu *padding* là *int* : mặc định trái, phải, trên, dưới sẽ bằng *padding*.
        - Nếu *padding* là *Tuple[int, int, int, int]* : các giá trị theo thứ tự lần lượt là left, right, top, bottom.

        :param surface: Một thể thiện của pygame.Surface.
        :param padding: Tăng viền cho surface.
        :param color: Màu của viền mới.
        :return: Một pygame.Surface mới.
        """

        size = surface.get_size()
        if type(padding) is int:
            bg = ImageProcessor.surface((size[0] + padding * 2, size[1] + padding * 2), color)
            bg.blit(surface, (padding, padding))
        else:
            bg = ImageProcessor.surface((size[0] + padding[0] + padding[1], size[1] + padding[2] + padding[3]), color)
            bg.blit(surface, (padding[0], padding[2]))

        return bg

    @staticmethod
    def rect(
        rectangle: Union[pygame.Surface, Tuple[int, int]],
        color: Tuple[int, int, int, int],
        width=0,
        border_radius=-1,
        border_top_left_radius=-1,
        border_top_right_radius=-1,
        border_bottom_left_radius=-1,
        border_bottom_right_radius=-1
    ):
        """ Phương thức **rect** : trả về ảnh của một hình chữ nhật ( có thể tùy chọn ).\n

        - Nếu **rectangle** là *Tuple[int, int]* : nó sẽ tạo một *pygame.Surface* mới với kích thước **rectangle**.
        - Nếu **rectangle** là *pygame.Surface* : nó sẽ vẽ **rectangle** đè lên hình chữ nhật mới vẽ.
        - Nếu **width** = 0 : hình chữ nhật sẽ lấp đầy bằng *color*.
        - Nếu **width** != 0 : hình ảnh sẽ chỉ có viền của hình chữ nhật với độ dày là **width**.
        - Các tham số *border* : độ bo tròn các góc của hình chữ nhật.

        :param rectangle: một dạng hình chữ nhật, có thể là kích thước, hoặc một pygame.Surface.
        :param color: Tuple[int, int, int, int]
        :param width: int
        :param border_radius: int
        :param border_top_left_radius: int
        :param border_top_right_radius: int
        :param border_bottom_left_radius: int
        :param border_bottom_right_radius: int
        :return: pygame.Surface
        """

        is_size = type(rectangle) is tuple
        if is_size:
            surface = ImageProcessor.surface(rectangle)
        else:
            surface = ImageProcessor.surface(rectangle.get_size())

        pygame.draw.rect(surface, color, (0, 0) + surface.get_size(), width, border_radius,
                         border_top_left_radius, border_top_right_radius,
                         border_bottom_left_radius, border_bottom_right_radius)

        if not is_size:
            surface.blit(rectangle, (0, 0))
        return surface

    @staticmethod
    def circle(
        radius: int,
        color: Tuple[int, int, int, int],
        width=0,
        rectangle: pygame.Surface = None
    ):
        """ Phương thức **circle** : trả về ảnh của một hình tròn có bán kính là *radius*.\n

        - Nếu **width** = 0 : hình ảnh sẽ lấp đầy bằng **color**.
        - Nếu **width** != 0 : hình ảnh sẽ chỉ có viền của hình tròn với độ dày là **width**.
        - Nếu **rectangle** != None : nó sẽ vẽ **rectangle** đè lên hình tròn mới vẽ.

        :param radius: Bán kính hình tròn.
        :param color: Màu sắc của hình tròn.
        :param width: Độ dày của hình tròn.
        :param rectangle: Một pygame.Surface.
        :return: pygame.Surface
        """

        surface = ImageProcessor.surface((radius * 2, radius * 2))
        pygame.draw.circle(surface, color, (radius, radius), radius, width)
        if rectangle:
            surface.blit(rectangle, (0, 0))
        return surface

    @staticmethod
    def fill_mask(
        surface: pygame.Surface,
        color: Tuple[int, int, int, int],
        mask: pygame.mask.Mask = None
    ):
        """ Phương thức **fill_mask**: vẽ đè lên các điểm ảnh của một vật thể bằng *color*.

        :param surface: pygame.Surface
        :param color: Tuple[int, int, int, int]
        :param mask: pygame.mask.Mask
        :return: pygame.Surface
        """

        size = surface.get_size()
        if not mask:
            mask = pygame.mask.from_surface(surface)
        fill_surface = ImageProcessor.surface(size, color)

        for i in range(size[0]):
            for j in range(size[1]):
                if mask.get_at((i, j)):
                    fill_surface.set_at((i, j), color)
        return fill_surface

    @staticmethod
    def square(surface: pygame.Surface, centroid=Vector2.zero()):
        """ Phương thức **square** : tạo một ảnh kích thước hình vuông , với tâm là tâm *surface* - *centroid*.

        :param surface: pygame.Surface
        :param centroid: Vector2
        :return: pygame.Surface
        """

        size = surface.get_size()
        centroid_vector = (size[0] / 2 + centroid[0], size[1] / 2 + centroid[1])
        x1, x2 = abs(centroid_vector[0]), abs(centroid_vector[0] - size[0])
        y1, y2 = abs(centroid_vector[1]), abs(centroid_vector[1] - size[1])
        edge = int(max(x1, x2, y1, y2))

        new_surface = ImageProcessor.surface((edge * 2, edge * 2))
        new_surface.blit(surface, Vector2(edge, edge) - centroid_vector)
        return new_surface


class Image:
    """ Lớp **Image** : lưu và hiển thị hình ảnh ( tương tự như *pygame.Surface* ) trong trò chơi. """

    __doc__ = 'Class Image : storage image, mask, position of Surface.'

    def __init__(
        self,
        surface: pygame.Surface,
        position: Union[Vector2, Tuple[int, int]]
    ):
        self._SURFACE = surface                     # Lưu hình ảnh gốc ( không thay đổi dữ liệu gốc )
        self._surface = surface                     # Lưu hình hiển thị ( sẽ có thay đổi )

        self._mask = pygame.mask.from_surface(surface)
        self._rect = surface.get_rect()
        self._rect.center = position

    @property
    def surface(self):
        return self._surface

    @property
    def mask(self):
        return self._mask

    @property
    def rect(self):
        return self._rect

    @property
    def size(self):
        return self._rect.size

    @property
    def width(self):
        return self._rect.width

    @property
    def height(self):
        return self._rect.height

    def _change_surface(self, surface: pygame.Surface):
        """ Phương thức **_change_surface** : thay đổi hình ảnh sẽ hiển thị của nó.

        :param surface: pygame.Surface
        :return: None
        """

        self._surface = surface
        position = self._rect.center
        self._rect = surface.get_rect()
        self._rect.center = position
        self._mask = pygame.mask.from_surface(surface)

    def blit_to(self, parent):
        """ Phương thức **blit_to** : vẽ nó lên vật thể parent.

        :param parent: Image or pygame.Surface
        :return: None
        """

        if type(parent) is Image or isinstance(parent, Image):
            parent.surface.blit(self._surface, self._rect.topleft)
        elif type(parent) is pygame.Surface:
            parent.blit(self._surface, self._rect.topleft)

    def fill_mask(self, color: Tuple[int, int, int, int]):
        """ Phương thức **fill_mask** : chỉ vẽ đè lên các điểm ảnh của vật thể.

        :param color: Tuple[int, int, int, int]
        :return: None
        """

        fill_surface = ImageProcessor.fill_mask(self._surface, color)
        self._surface.blit(fill_surface, (0, 0))

    def collide_point(self, point: Union[Vector2, Tuple[int, int]]):
        """ Phương thức **collide_point** : trả về True nếu *point* nằm trong hình chữ nhật.

        :param point: Vector2 or Tuple[int, int]
        :return: bool
        """

        return self._rect.collidepoint(point)

    def mask_collide_point(self, point: Union[Vector2, Tuple[int, int]]):
        """ Phương thức **mask_collide_point** : trả về True nếu *point* nằm trong các điểm ảnh.

        :param point: Vector2 or Tuple[int, int]
        :return: bool
        """

        top_left = self._rect.topleft

        x = int(point[0] - top_left[0])
        if x < 0 or x >= self.width:
            return False
        y = int(point[1] - top_left[1])
        if y < 0 or y >= self.height:
            return False
        return bool(self._mask.get_at((x, y)))

    def update(self, action=True):
        """ Phương thức **update** : cập nhật hình ảnh trên màn hình.

        :param action: bool
        :return: None
        """

        app.screen.blit(self._surface, self._rect)

    def scale(self, new_size: Union[int, float, Tuple[int, int], Tuple[float, float]]):
        """ Phương thức **scale** : phóng to hoặc thu nhỏ hình ảnh với tỷ lệ hoặc kích thước được cung cấp.\n
        - Nếu **new_size** là *int* hoặc *float* : kích thước mới bằng kích thước cũ nhân với **new_size**.\n
        - Nếu **new_size** là *Tuple[float, float]* :
        kích thước cũ là *(w, h)* và **new_size** là *(per_w, per_h)* -> kích thước mới là *(w * per_w, h * per_h)*.\n
        - Nếu **new_size** là *Tuple[int, int]* : kích thước mới bằng chính **new_size**.

        :param new_size: int, float or Tuple[int, int] or Tuple[float, float]
        :return: pygame.Surface
        """

        flip_x = flip_y = False
        size = new_size

        if type(new_size) is int or type(new_size) is float:        # Scale image with 'new_size' percent
            size = (int(self.width * new_size), int(self.height * new_size))

            if new_size < 0:
                flip_x = flip_y = True
        elif type(new_size) is tuple:
            if new_size[0] < 0:
                flip_x = True
            if new_size[1] < 0:
                flip_y = True

            if type(new_size[0]) is int:                            # Scale image with size is 'new_size'
                size = (abs(new_size[0]), abs(new_size[1]))
            elif type(new_size[0]) is float:
                size = (abs(int(self.width * new_size[0])), abs(int(self.height * new_size[1])))

        if flip_x or flip_y:
            self._SURFACE = pygame.transform.flip(self._SURFACE, flip_x, flip_y)
        self._change_surface(pygame.transform.scale(self._SURFACE, size))


class Label(Image):
    """Lớp **Label** : lưu văn bản dạng hình ảnh."""

    # Cung cấp các kiểu chữ : đậm, nghiêng, gạch chân, ...
    STYLE_DEFAULT = pygame.freetype.STYLE_DEFAULT
    STYLE_UNDERLINE = pygame.freetype.STYLE_UNDERLINE
    STYLE_OBLIQUE = pygame.freetype.STYLE_OBLIQUE
    STYLE_NORMAL = pygame.freetype.STYLE_NORMAL
    STYLE_STRONG = pygame.freetype.STYLE_STRONG
    STYLE_WIDE = pygame.freetype.STYLE_WIDE

    __doc__ = 'Class Label : storage title in surface, font size, style of text, position, size of label.'

    def __init__(
        self,
        text: str,
        font_size: Union[int, float],
        position: Union[Vector2, Tuple[int, int]],
        color=Color.White,
        style=pygame.freetype.STYLE_DEFAULT,
        font_name: Font = Resource.font_name
    ):
        """ Khởi tạo **Label** : nhận vào các tham số để khởi tạo một **Label**.

        :param text: Văn bản.
        :param font_size: Cỡ chữ.
        :param position: Vị trí hiển thị.
        :param color: Màu chữ.
        :param style: Kiểu chữ.
        :param font_name: Tên phông chữ.
        """

        self._FONT: Font = font[font_name]
        self._color = color
        self._text = text
        self._font_size = font_size
        self._style = style

        super().__init__(self._FONT.render(text, color, style=style, size=font_size)[0], position)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, new_text: str):
        if self._text != new_text:
            self._text = new_text
            self._change_surface()

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, new_color):
        if self._color != new_color:
            self._color = new_color
            self._change_surface()

    @property
    def font_size(self):
        return self._font_size

    @font_size.setter
    def font_size(self, new_font_size: Union[int, float]):
        if self._font_size != new_font_size:
            self._font_size = new_font_size
            self._change_surface()

    def _change_surface(self, surface: pygame.Surface = None):
        if not surface:
            surface = self._FONT.render(self._text, self._color, size=self._font_size, style=self._style)[0]
        super(Label, self)._change_surface(surface)

    def set_up(
        self,
        new_text: str = None,
        new_color: Tuple[int, int, int, int] = None,
        new_font_size: Union[int, float] = None
    ):
        ''' Phương thức **set_up** : thay đổi văn bản, màu chữ, hoặc kích cỡ.

        :param new_text: Văn bản mới.
        :param new_color: Màu chữ mới.
        :param new_font_size: Kích cỡ chữ mới.
        :return: None
        '''

        is_change = False
        if new_text and self._text != new_text:
            self._text = new_text
            is_change = True
        if new_color and self._color != new_color:
            self._color = new_color
            is_change = True
        if new_font_size and self._font_size != new_font_size:
            self._font_size = new_font_size
            is_change = True
        if is_change:
            self._change_surface()


class TimerClick:
    """Lớp **TimerClick** : đặt thời gian dựa trên một biến của một *GameObject*."""

    Timer = type('Timer', (), {'tick': True})

    __doc__ = 'Lớp Timer : đặt thời gian dựa trên một biến của một *GameObject*.'

    def __init__(self, time_wait: int, parent=Timer(), var_name: str = 'tick'):
        """ Khởi tạo lớp **TimerClick**.

        :param time_wait: Thời gian cài đặt ( tính bằng giây ).
        :param var_name: Tên một trường của object parent.
        :param parent: Đặt thời gian dựa trên parent.
        """

        assert hasattr(parent, var_name), f'Tham số parent không tồn tại trường có tên {var_name} !.'

        self.__parent = parent
        self.__var_name = var_name
        self.__time_wait = time_wait
        self.__count_time = time_wait
        self.tick = False

    def update(self, action=True):
        if getattr(self.__parent, self.__var_name):
            self.__count_time += app.time.delta_time_milliseconds

            if self.__count_time >= self.__time_wait:
                self.tick = True
                self.__count_time -= self.__time_wait
            else:
                self.tick = False
        else:
            if self.__count_time < self.__time_wait:
                self.__count_time += app.time.delta_time_milliseconds
            self.tick = False


class FPSLabel(Image):
    """Lớp **FPSLabel** : hiển thị *FPS* của ứng dụng."""

    __doc__ = 'Lớp FPSLabel : hiển thị số FPS của khung hình.'

    def __init__(
            self,
            font_size: float,
            position: Union[Vector2, Tuple[int, int]],
            color=Color.White,
            time_wait: int = 1000,
            style=Label.STYLE_DEFAULT,
            font_name=Resource.font_name
    ):
        self._timer = TimerClick(time_wait)
        src_font: Font = font[font_name]
        label_size = src_font.get_rect('FPS: 60', style, size=font_size).size

        rect = ImageProcessor.rect((label_size[0] * 1.3, label_size[1] * 3), color, 1, 8)
        super().__init__(rect, position)
        self._label = Label(f'FPS: {int(app.time.fps)}', font_size, position, color, style, font_name)

    @property
    def position(self):
        return self._rect.center

    @position.setter
    def position(self, new_position: Union[Vector2, Tuple[int, int]]):
        self._rect.center = new_position
        self._label.rect.center = new_position

    def _change_surface(self, surface: pygame.Surface = None):
        self._label.text = f'FPS: {int(app.time.fps)}'

    def update(self, action=False):
        self._timer.update()
        if self._timer.tick:
            self._change_surface()

        app.screen.blit(self._surface, self._rect.topleft)
        self._label.update()


class CursorIcon(ABC):
    """Class **CursorIcon** : lớp tổng quát cho các lớp thay thế chuột máy tính."""

    __doc__ = 'Lớp CursorIcon : lớp tổng quát cho các icon chuột máy tính.'

    def __init__(self, cursor_image: pygame.Surface, cursor_click_image: pygame.Surface):
        self._cursor_image = cursor_image
        self._cursor_click_image = cursor_click_image

    @abstractmethod
    def update(self): pass


class CursorImage(CursorIcon):
    """Class **CursorImage** : thay chuột máy tính thành ảnh tự chọn."""

    __doc__ = 'Lớp CursorImage : thay chuột máy tính bằng một hình ảnh khác.'

    @staticmethod
    def find_outline(outline: List[Tuple[int, int]]):
        x, y = outline[0]
        for point in outline:
            if x > point[0] and y > point[1]:
                x, y = point
        return -x, -y

    def __init__(
        self,
        cursor_image: pygame.Surface,
        cursor_click_image: pygame.Surface = None
    ):
        super().__init__(cursor_image, cursor_click_image)
        self.dist_cursor = CursorImage.find_outline(pygame.mask.from_surface(cursor_image).outline())
        if cursor_click_image:
            self.dist_cursor_click = CursorImage.find_outline(pygame.mask.from_surface(cursor_click_image).outline())

    def update(self):
        top_left = app.cursor.position + self.dist_cursor_click

        if app.cursor.multi_left and self._cursor_click_image:
            app.screen.blit(self._cursor_click_image, top_left)
        else:
            app.screen.blit(self._cursor_image, top_left)


class CursorShoot(CursorIcon):
    """Class **CursorShoot** : thay chuột máy tính thành ảnh nòng ngắm."""

    __doc__ = 'Lớp CursorShoot : thay chuột máy tính thành ảnh nòng ngắm.'

    def __init__(self):
        surf = ImageProcessor.surface((25, 25))
        pygame.draw.line(surf, Color.White, (0, 12), (10, 12), 3)
        pygame.draw.line(surf, Color.White, (14, 12), (24, 12), 3)
        pygame.draw.line(surf, Color.White, (12, 0), (12, 10), 3)
        pygame.draw.line(surf, Color.White, (12, 14), (12, 24), 3)
        pygame.draw.line(surf, Color.White, (12, 12), (12, 12), 3)

        surf_click = pygame.Surface((35, 35), pygame.SRCALPHA)
        surf_click.blit(surf, (5, 5))
        pygame.draw.circle(surf_click, Color.White, (17, 17), 20, 2)

        super().__init__(surf, surf_click)
        self.dist_cursor = (-12, -12)
        self.dist_cursor_click = (-17, -17)

    def update(self):
        if app.cursor.multi_left and self._cursor_click_image:
            app.screen.blit(self._cursor_click_image, app.cursor.position + self.dist_cursor_click)
        else:
            app.screen.blit(self._cursor_image, app.cursor.position + self.dist_cursor)
