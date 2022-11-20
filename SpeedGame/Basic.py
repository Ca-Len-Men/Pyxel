__doc__ = '''           Ngày tạo : 14/11/2022.
File Basic.py    : định nghĩa các lớp cơ bản hỗ trợ viết game.
Lớp StaticClassMeta : như tên của nó, nó muốn các lớp con kế thừa phải là tĩnh
                      ( tức là không thể khởi tạo biến ).
Lớp Color           : nó định nghĩa sẵn các biến màu cơ bản ( nó là lớp tĩnh ).
Lớp Math            : nó định nghĩa sẵn các hàm tính toán, các công thức toán học ( nó là lớp tĩnh ).
Lớp Vector          : một kiểu dữ liệu quan trọng trong việc viết game.
'''

import math
from Rule import SingletonMeta, StaticClassMeta, Resource, load_asset
from typing import Union, Tuple
from random import randint, random
from pygame.freetype import Font
from pygame.image import load

__version__ = '1.0.0'


class Color(metaclass=StaticClassMeta):
    """Lớp **Color** : cung cấp các màu sắc mặc định."""

    # Màu cơ bản
    NoColor = (0, 0, 0, 0)
    Red = (255, 0, 0, 255)
    Pink = (255, 192, 203, 255)
    Yellow = (255, 255, 0, 255)
    Orange = (255, 165, 0, 255)
    Green = (0, 255, 0, 255)
    Blue = (0, 0, 255, 255)
    Purple = (128, 0, 128, 255)
    White = (255, 255, 255, 255)
    Gray = (190, 190, 190, 255)
    Black = (0, 0, 0, 255)

    # Màu Boostrap
    Primary = (13, 110, 253, 255)
    Secondary = (108, 117, 125, 255)
    Success = (25, 135, 84, 255)
    Danger = (220, 53, 69, 255)
    Warning = (255, 193, 7, 255)
    Info = (13, 202, 240, 255)
    Light = (248, 249, 250, 255)
    Dark = (33, 37, 41, 255)

    # Các màu khác
    Gold = (255, 215, 0, 255)
    LightBlue = (173, 216, 230, 255)
    LightCyan = (224, 255, 255, 255)
    DarkCyan = (0, 139, 139, 255)
    LightGreen = (144, 238, 144, 255)
    GreenYellow = (173, 255, 47, 255)
    Chocolate = (255, 127, 36, 255)
    Violet = (238, 130, 238, 255)

    @staticmethod
    def __doc__():
        return 'Class Color : cung cấp các màu sắc mặc định.'

    @staticmethod
    def color_alpha(color: Tuple[int, int, int, int], alpha: int):
        return color[0], color[1], color[2], alpha

    # Random màu sắc
    @staticmethod
    def random():
        return randint(0, 255), randint(0, 255), randint(0, 255)


class Math(metaclass=StaticClassMeta):
    """Class **Math** : lớp hỗ trợ tính toán, các công thức toán học."""

    __doc__ = 'Lớp Math : hỗ trợ các hàm tính toán, các công thức toán học.'

    # Phương thức angle : tính góc của một Vector2.
    # Kết quả trả về có giá trị trong đoạn [0, 360].
    @staticmethod
    def angle(vector2d: Tuple[Union[int, float], Union[int, float]]):
        degrees = math.degrees(math.atan2(vector2d[1], vector2d[0]))
        return degrees + 360 if degrees < 0 else degrees

    # Phương thức vector : trả về một vector độ dài 1 với một góc được chỉ định.
    @staticmethod
    def vector(degrees: float):
        degrees %= 360
        if degrees < 0:
            degrees += 360

        y = math.sin(math.radians(degrees))
        x = math.sqrt(1 - y ** 2)
        return (-x, y) if 90 < degrees < 270 else (x, y)

    # Phương thức move_to_ward : tịnh tiến một giá trị current tới target một khoảng delta.
    @staticmethod
    def move_to_ward(current: float, target: float, delta: float):
        if abs(current - target) <= delta:
            return target
        else:
            return current + delta if current < target else current - delta


class Vector2:
    """Class **Vector2** : thể hiện cho *vector* trong mặt phẳng, có thể là một điểm hoặc một hướng đi."""

    __doc__ = '''Lớp Vector2 : 
    - Thể hiện cho một điểm trong mặt phẳng ( thay thế cho Tuple[int, int] ).
    - Thể hiện cho một vector có hướng trong mặt phẳng.
    - Hỗ trợ các toán tử cộng, trừ, nhân, chia, ... giữa hai Vector2.
    - Hỗ trợ các hàm tính toán liên quan trong mặt phẳng.
    '''

    def __init__(self, x: Union[int, float], y: Union[int, float]):
        self.x = x
        self.y = y

    @classmethod
    def zero(cls):
        return cls(0, 0)

    @classmethod
    def left(cls):
        return cls(-1, 0)

    @classmethod
    def right(cls):
        return cls(1, 0)

    @classmethod
    def up(cls):
        return cls(0, -1)

    @classmethod
    def down(cls):
        return cls(0, 1)

    # Tạo ngẫu nhiên một Vector có độ dài 1.
    @classmethod
    def random(cls):
        x = random()
        y = 1 - x ** 2
        return Vector2(x, y) if randint(0, 1) == 0 else Vector2(x, -y)

    # Property angle : get hoặc set chỉ số góc của Vector.
    @property
    def angle(self):
        return Math.angle((self.x, self.y))

    @angle.setter
    def angle(self, degrees: float):
        if bool(self) is False:     # Vector equals (0, 0)
            return

        length = float(self)        # Length of Vector
        self.x, self.y = Math.vector(degrees)   # Length of vector equals 1, angle's vector is degrees
        if length != 1:
            self.x *= length
            self.y *= length

    # Sao chép một biến Vector mới.
    def copy(self):
        return self.__copy__()

    # Tính khoảng cách giữa hai Vector.
    def dist(self, other) -> float:
        return float(self.__sub__(other))

    # Thay đổi Vector có độ dài là 1.
    def normalize(self):
        distance = self.__float__()
        return Vector2(self.x / distance, self.y / distance)

    # Tịnh tiến điểm Vector này tới một điểm Vector khác một khoảng delta.
    def move_to_ward(self, target, delta: Union[int, float]):
        if delta == 0:
            return

        sub = self.__sub__(target)
        if sub.__float__() <= delta:
            self.x, self.y = target.x, target.y
        else:
            move_vector = sub.normalize() * delta
            self.x -= move_vector.x
            self.y -= move_vector.y

    @property
    def tuple(self):
        return self.x, self.y

    @tuple.setter
    def tuple(self, new_tuple: Union[Tuple[int, int], Tuple[float, float]]):
        self.x, self.y = new_tuple

    # Sao chép Vector từ một kiểu dữ liệu bất kỳ.
    @classmethod
    def copy_from(cls, point):
        return cls(point[0], point[1])

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __repr__(self):
        return f'({self.x}, {self.y})'

    def __len__(self):
        return 2

    def __copy__(self):
        return Vector2(self.x, self.y)

    def __add__(self, other):
        return Vector2(self.x + other[0], self.y + other[1])

    def __iadd__(self, other):
        return Vector2(self.x + other[0], self.y + other[1])

    def __sub__(self, other):
        return Vector2(self.x - other[0], self.y - other[1])

    def __isub__(self, other):
        return Vector2(self.x - other[0], self.y - other[1])

    def __mul__(self, val: Union[int, float, Tuple[float, float]]):
        if type(val) is tuple:
            return Vector2(self.x * val[0], self.y * val[1])
        return Vector2(self.x * val, self.y * val)

    def __imul__(self, val: Union[int, float, Tuple[float, float]]):
        if type(val) is tuple:
            return Vector2(self.x * val[0], self.y * val[1])
        return Vector2(self.x * val, self.y * val)

    def __truediv__(self, val: Union[int, float, Tuple[float, float]]):
        if type(val) is tuple:
            return Vector2(self.x / val[0], self.y / val[1])
        return Vector2(self.x / val, self.y / val)

    def __itruediv__(self, val: Union[int, float, Tuple[float, float]]):
        if type(val) is tuple:
            return Vector2(self.x / val[0], self.y / val[1])
        return Vector2(self.x / val, self.y / val)

    def __floordiv__(self, val: Union[int, float]):
        return Vector2(self.x // val, self.y // val)

    def __ifloordiv__(self, val: Union[int, float]):
        return Vector2(self.x // val, self.y // val)

    def __abs__(self):
        return Vector2(abs(self.x), abs(self.y))

    def __bool__(self):
        return self.x != 0 or self.y != 0

    def __eq__(self, other):
        return self.x == other[0] and self.y == other[1]

    def __ne__(self, other):
        return self.x != other[0] or self.y != other[1]

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    def __float__(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __getitem__(self, i: int):
        return self.x if i % 2 == 0 else self.y

    def __setitem__(self, i: int, value: Union[int, float]):
        if i % 2 == 0:
            self.x = value
        else:
            self.y = value


class IconStore(metaclass=SingletonMeta):
    __doc__ = 'Lớp IconStore : lưu trữ các hình ảnh mặc định của module.'

    # Phương thức tải Asset Icon : mỗi lần được gọi là một lần tải mới.
    @load_asset(Resource.icon_dir)
    def __getitem__(self, asset_name):
        return load(asset_name)


class FontStore(metaclass=SingletonMeta):
    __doc__ = 'Lớp FontStore : lưu trữ các phông chữ mặc định của module.'

    # Phương thức tải Asset Font : chỉ tải lên một lần duy nhất trong lần gọi đầu tiên.
    @load_asset(Resource.font_dir)
    def __getitem__(self, asset_name):
        if asset_name not in Resource.font_save:
            Resource.font_save[asset_name] = Font(asset_name)
        return Resource.font_save[asset_name]


icon = IconStore()
font = FontStore()
