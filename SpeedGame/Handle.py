__doc__ = '''           Ngày tạo : 15/11/2022
File Handle.py      : định nghĩa các lớp điều khiển, quản lý.
Lớp SingletonMeta   : nó muốn các lớp con kế thừa chỉ có thể khởi tạo một lần duy nhất.
Lớp CursorHandle    : quản lý các sự kiện chuột máy tính.
'''

import pygame
from pygame import freetype
from Rule import SingletonMeta
from Basic import Vector2, Color, randint, Union, Tuple

__version__ = '1.0.0'


# Class CursorController : quản lý các sự kiện của chuột bàn phím.
class CursorHandle(metaclass=SingletonMeta):
    @staticmethod
    def __doc__():
        return 'Class CursorController : quản lý các sự kiện chuột bàn phím.'

    get_visible = pygame.mouse.get_visible
    set_visible = pygame.mouse.set_visible

    def __init__(self):
        # Biến click : sự kiện nhấp nhả chuột.
        # Biến multi_click : sự kiện nhấp chuột liên tục.

        self.__right_click = self.__right_multi_click = False
        self.__left_click = self.__left_multi_click = False
        self.__pressed_right = self.__pressed_left = False
        self.__position = Vector2(0, 0)

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, new_position: Union[Vector2, Tuple[int, int]]):
        self.__position = new_position
        pygame.mouse.set_pos(new_position)

    # Kiểm tra nhấp nhả chuột trái
    @property
    def left(self):
        return self.__left_click

    # Kiểm tra nhấp nhả chuột phải
    @property
    def right(self):
        return self.__right_click

    # Kiểm tra đè chuột trái
    @property
    def multi_left(self):
        return self.__left_multi_click

    # Kiểm tra đè chuột phải
    @property
    def multi_right(self):
        return self.__right_multi_click

    def update(self, action=True):
        """ Phương thức **update** : cập nhật các sự kiện chuột bàn phím trên mỗi khung hình.

        :param action: bool
        :return: None
        """

        # Lấy vị trí chuột
        self.__position.tuple = pygame.mouse.get_pos()

        # Sự kiện nhấp chuột
        result = pygame.mouse.get_pressed(num_buttons=3)
        self.__left_multi_click = result[0]
        self.__right_multi_click = result[2]

        if result[0]:  # Left click
            if not self.__pressed_left:
                self.__left_click = True
                self.__pressed_left = True
            else:
                self.__left_click = False
        else:
            self.__pressed_left = False

        if result[2]:  # Right click
            if not self.__pressed_right:
                self.__right_click = True
                self.__pressed_right = True
            else:
                self.__right_click = False
        else:
            self.__pressed_right = False

    def refresh(self):
        """ Phương thức **refresh** : làm mới các sự kiện chuột bàn phím.

        :return: None
        """

        self.__right_click = self.__right_multi_click = False
        self.__left_click = self.__left_multi_click = False


# Class TimeHandle : quản lý thời gian của chương trình.
class TimeHandle(metaclass=SingletonMeta):
    @staticmethod
    def __doc__():
        return 'Class TimeHandle : quản lý thời gian của chương trình.'

    def __init__(self):
        self.__clock = pygame.time.Clock()
        self.__fps = 0
        self.__deltaTime = 0
        self.__deltaTime_millisecond = 0

    @property
    def fps(self):
        return self.__clock.get_fps()

    @fps.setter
    def fps(self, new_fps):
        self.__fps = new_fps

    @property
    def delta_time(self):
        return self.__deltaTime

    @property
    def delta_time_milliseconds(self):
        return self.__deltaTime_millisecond

    def update(self, action=True):
        """ Phương thức **update** : cập nhật các sự kiện thời gian trong mỗi khung hình.

        :param action: bool
        :return: None
        """

        self.__deltaTime_millisecond = self.__clock.tick(self.__fps)
        self.__deltaTime = self.__deltaTime_millisecond / 1000


# Lớp quản lí chương trình ứng dụng.
class GameHandle(metaclass=SingletonMeta):
    @staticmethod
    def __doc__():
        return 'Lớp quản lí trò chơi ứng dụng.'

    def __init__(self):
        self.__screen = None                    # Màn hình ứng dụng
        self.cursor_display = None              # Hiển thị chuột
        self.time = TimeHandle()                # Quản lý time
        self.cursor = CursorHandle()            # Quản lý cursor

        pygame.freetype.init()

    @property
    def screen(self) -> pygame.Surface:
        return self.__screen

    @property
    def size(self):
        return self.__screen.get_size()

    @property
    def width(self):
        return self.__screen.get_width()

    @property
    def height(self):
        return self.__screen.get_height()

    @property
    def random_position(self):
        return randint(0, self.width - 1), randint(0, self.height - 1)

    ''' Hãy gọi hàm init trước khi cho trò chơi hoạt động. '''
    def init(
        self,
        size: Tuple[int, int],
        caption: str = None,
        icon_path: str = None
    ):
        """ Phương thức **init** : khởi tạo các thông số cho ứng dụng.

        :param size: Kích thước màn hình.
        :param caption: Tên ứng dụng.
        :param icon_path: ảnh đại diện cho ứng dụng.
        :return: None
        """

        pygame.display.init()

        self.__screen = pygame.display.set_mode(size)
        if caption:
            pygame.display.set_caption(caption)
        if icon_path:
            pygame.display.set_icon(pygame.image.load(icon_path))

    def update(self):
        """ Phương thức **update** : cập nhật các thông số, sự kiện trên từng khung hình.

        :return: None
        """

        # Sự kiện đóng ứng dụng
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        self.time.update()
        self.cursor.update()
        if self.cursor_display:
            self.cursor_display.update()

        # Cập nhật ứng dụng
        pygame.display.update()

    def draw_line(
        self,
        at: Union[Vector2, Tuple[Union[int, float], Union[int, float]]],
        vector: Union[Vector2, Tuple[Union[int, float], Union[int, float]]],
        color=Color.White,
        width=1
    ) -> None:
        pygame.draw.line(self.__screen, color, at, at + vector, width)

    def blit(
        self,
        surface: pygame.Surface,
        position=(0, 0)
    ) -> None:
        if type(surface) is pygame.Surface:
            self.__screen.blit(surface, position)


# Khởi tạo lớp quản lý trò chơi.
app = GameHandle()
