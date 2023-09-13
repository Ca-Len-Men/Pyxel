from .fmath import *

from weakref import WeakMethod
import random

class WeakrefMethod:
    """
    - Lớp này lưu một 'weakref method'
    -> Mục đích : khi một object cần được giải phóng, tránh việc còn giữ 'bounded method' khiến object vẫn tồn tại.
    """

    def __init__(self, __bounded_method):
        self.__weakref_bounded_method = WeakMethod(__bounded_method)

    def __call__(self, *args):
        """
        - Gọi đến 'bounded method' khi khởi tạo, truyền vào đó các tham số 'args'.
        - Nếu object vẫn còn tồn tại, trả về True.
        """

        __callable = self.__weakref_bounded_method()
        if __callable:
            __callable(*args)
        return __callable is not None

class Delegate:
    """
    - Lớp này lưu nhiều 'WeakrefMethod'.
    - Khi một 'WeakrefMethod' "chết" đi, nó xóa 'WeakrefMethod' đó ra khỏi tập lưu trữ.
    """

    def __init__(self):
        self._weakref_methods = None  # type: ignore

    def call(self, *args):
        """
        - Hàm này được gọi khi một "sự kiện/thay đổi" xảy ra,
        nó gọi đến các "hành động" ( bounded method ) mà nó lưu trữ ( cùng tham số 'args' ).
        - Nếu một "hành động" chết đi, xóa "hành động" đó khỏi tập lưu trữ.
        """

        if self._weakref_methods is None:
            return

        # Tạo thùng rác, lưu những "hành động chết"
        recycle_bin = None

        # Gọi đến các "hành động"
        for __callable in self._weakref_methods:  # type: ignore
            __alive = __callable(*args)

            # "Hành động" này đã "chết"
            if not __alive:
                if recycle_bin is None:
                    recycle_bin = set()
                recycle_bin.add(__callable)

        # Xóa những "hành động chết" ra khỏi tập lưu trữ
        if recycle_bin:
            self._weakref_methods -= recycle_bin

    def add(self, __weakref_bounded_method):
        """
        - Thêm một "hành động" cho một "sự kiện".
        """

        assert isinstance(__weakref_bounded_method, WeakrefMethod), \
            f"From {self.__class__.__name__}.add : " \
            f"parameter type of '__weakref_bounded_method' must be <WeakrefMethod> !"

        if self._weakref_methods is None:
            self._weakref_methods = set()
        self._weakref_methods.add(__weakref_bounded_method)


class Vector:
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

    @classmethod
    def random(cls):
        x = random.random()
        y = 1 - x * x
        return cls(x, y) if random.randint(0, 1) else cls(x, -y)

    def __init__(self, __x, __y):
        self.__x = __x
        self.__y = __y

    # BASE
    def setxy(self, __x, __y):
        """
        - Phương thức dùng để thay đổi thuộc tính x, y của Vector.
        - Mọi thay đổi trên thuộc tính x, y của Vector đều phải gọi qua phương thức này
        -> Mục đích : ghi đè phương thức này ở các lớp con.
        """

        self.__x = __x
        self.__y = __y

    def set(self, source):
        if isinstance(source, (Vector, tuple, list)):
            self.setxy(*source)
        else:
            raise TypeError(f'From {self.__class__.__name__}.set : '
                            f'parameter type `source` must be <tuple, list, Vector> !')

    @property
    def x(self):
        return self.__x

    @x.setter   # type: ignore
    def x(self, __x):
        self.setxy(__x, self.y)

    @property
    def y(self):
        return self.__y

    @y.setter   # type: ignore
    def y(self, __y):
        self.setxy(self.x, __y)

    @property
    def angle(self):
        return angle(self.x, self.y)

    @angle.setter   # type: ignore
    def angle(self, __angle):
        if relative_compare(self.x, 0) and relative_compare(self.y, 0):
            raise ValueError(f"From {self.__class__.__name__}.angle : "
                             f"cannot determine the angle of vector (0, 0) !")

        length = magnitude(self.x, self.y)
        __x, __y = vector(__angle)
        self.setxy(__x * length, __y * length)

    @property
    def tup(self):
        return self.x, self.y

    @tup.setter # type: ignore
    def tup(self, __tup):
        self.setxy(*__tup)

    @property
    def tup_int(self):
        return int(self.x), int(self.y)

    @tup_int.setter # type: ignore
    def tup_int(self, __tup_int):
        self.setxy(*__tup_int)

    def copy(self):
        return Vector(self.x, self.y)

    def magnitude(self, other):
        return magnitude(self.x - other.x, self.y - other.y)

    def normalize(self):
        distance = magnitude(self.x, self.y)
        return Vector(self.x / distance, self.y / distance)

    def lerp(self, target, delta):
        __sub = Vector(target.x - self.x, target.y - self.y)
        __sub_distance = (__sub.x * __sub.x + __sub.y * __sub.y) ** .5

        if delta > 0 and __sub_distance <= delta:
            self.set(target)
            return True

        __value = delta / __sub_distance
        self.__iadd__(Vector(__sub.x * __value, __sub.y * __value))
        return False

    def __str__(self):
        return f'Vector({self.x}, {self.y})'

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return 2

    def __iter__(self):
        yield self.x
        yield self.y

    def __copy__(self):
        return self.copy()

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        self.setxy(self.x + other.x, self.y + other.y)
        return self

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __isub__(self, other):
        self.setxy(self.x - other.x, self.y - other.y)
        return self

    def __mul__(self, other):
        if isinstance(other, (Vector, tuple)):
            return Vector(self.x * other[0], self.y * other[1])
        elif isinstance(other, (float, int)):
            return Vector(self.x * other, self.y * other)

        raise TypeError(f'From {self.__class__.__name__}.__mul__ : '
                        f'type of parameter `other` must be <float, tuple or Vector> !')

    def __imul__(self, other):
        if isinstance(other, (tuple, Vector)):
            self.setxy(self.x * other[0], self.y * other[1])
        elif isinstance(other, (int, float)):
            self.setxy(self.x * other, self.y * other)
        else:
            raise TypeError(f'From {self.__class__.__name__}.__imul__ : '
                            f'type of parameter `other` must be <float, tuple, Vector> !')
        return self

    def __truediv__(self, val):
        return Vector(self.x / val, self.y / val)

    def __itruediv__(self, val):
        self.setxy(self.x / val, self.y / val)
        return self

    def __floordiv__(self, val):
        return Vector(self.x // val, self.y // val)

    def __ifloordiv__(self, val):
        self.setxy(self.x // val, self.y // val)
        return self

    def __abs__(self):
        return Vector(abs(self.x), abs(self.y))

    def __bool__(self):
        return not relative_compare(self.x, 0) or not relative_compare(self.y, 0)

    def __eq__(self, other):
        return relative_compare(self.x, other.x) and relative_compare(self.y, other.y)

    def __ne__(self, other):
        return not relative_compare(self.x, other.x) or not relative_compare(self.y, other.y)

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __float__(self):
        return magnitude(self.x, self.y)

    def __getitem__(self, i):
        if i == 0:
            return self.x
        elif i == 1:
            return self.y
        else:
            raise IndexError(f"From {self.__class__.__name__}.__getitem__ : "
                             f"Vector index out of range !")

    def __setitem__(self, i, value):
        if i == 0:
            self.setxy(value, self.y)
        elif i == 1:
            self.setxy(self.x, value)
        else:
            raise IndexError(f"From {self.__class__.__name__}.__getitem__ : "
                             f"Vector index out of range !")

class VectorListener(Vector):
    """
    - Vector này cho phép thực thi các hành động khi nó bị thay đổi ( x, y bị thay đổi ).
    """

    def __init__(self, __x, __y):
        super().__init__(__x, __y)
        self.__delegate = Delegate()

    def add_listener(self, __weakref_method):
        self.__delegate.add(__weakref_method)

    # Override
    def setxy(self, __x, __y):
        Vector.setxy(self, __x, __y)
        self.__delegate.call(self.copy())

    def only_set(self, source):
        """
        - Hàm này thay đổi x, y mà không gọi đến các hành động.
        """

        Vector.setxy(self, *source)

class VectorDependent(Vector):
    """
    - VectorDependent phụ thuộc tương đối vào một Vector khác, nghĩa là
    nó cách một Vector mà nó tham chiếu tới "một khoảng Vector".
    - Nếu nó không được tham chiếu đến Vector khác, mọi hành động đều như Vector thông thường.
    - (*) Sẽ có sai sót nếu chỉ chính nó tham chiếu đến Vector đó.
    """

    def __init__(self, __x, __y, __ref_vector=None):
        super().__init__(__x, __y)
        self.__ref_vector = __ref_vector

    # Override
    def setxy(self, __x, __y):
        # Không có tham chiếu
        if self.__ref_vector is None:
            Vector.setxy(self, __x, __y)
            return

        # Chính nó sẽ là "một khoảng Vector"
        # Lấy điểm cần "set" trừ đi Vector được tham chiếu
        Vector.setxy(self, __x - self.__ref_vector.x, __y - self.__ref_vector.y)

    def set_ref(self, __ref_vector):
        self.__ref_vector = __ref_vector

    # Override
    @property
    def x(self):
        __x = Vector.x.fget(self)
        # Không có tham chiếu
        if self.__ref_vector is None:
            return __x
        return self.__ref_vector.x + __x

    # Override
    @property
    def y(self):
        __y = Vector.y.fget(self)
        # Không có tham chiếu
        if self.__ref_vector is None:
            return __y
        return self.__ref_vector.y + __y
