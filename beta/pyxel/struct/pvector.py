# /**************************************************************************/
# /*  pvector.py                                                            */
# /**************************************************************************/
# /*                         This file is part of:                          */
# /*                                 PYXEL                                  */
# /*                  https://github.com/Ca-Len-Men/Pyxel                   */
# /**************************************************************************/

from pyxel.struct.pmath import *
from pyxel.struct.pdelegate import Delegate

import random

class Vector:
    @classmethod
    def zero(cls):
        return cls(0, 0)

    @classmethod
    def left(cls, length=1):
        return cls(-length, 0)

    @classmethod
    def right(cls, length=1):
        return cls(length, 0)

    @classmethod
    def up(cls, length=1):
        return cls(0, -length)

    @classmethod
    def down(cls, length=1):
        return cls(0, length)

    @classmethod
    def random(cls, length=1):
        x = random.random()
        y = 1 - x * x
        x *= length
        y *= length
        return cls(x, y) if random.randint(0, 1) else cls(x, -y)

    def __init__(self, __x: float, __y: float):
        self.__x = __x
        self.__y = __y
        self.__delegate = None

    # BASE
    def setxy(self, __x, __y):
        """
        - Phương thức dùng để thay đổi thuộc tính x, y của Vector.
        - Mọi thay đổi trên thuộc tính x, y của Vector đều phải gọi qua phương thức này
        -> Mục đích : ghi đè phương thức này ở các lớp con.
        """

        self.__x = __x
        self.__y = __y
        self.__delegate.call(self)

    @property
    def delegate(self):
        if self.__delegate is None:
            self.__delegate = Delegate()
        return self.__delegate

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
        return angle_of_vector(self.x, self.y)

    @angle.setter   # type: ignore
    def angle(self, __angle: float):
        if self.x is 0 and self.y is 0:
            raise ValueError(f"From {self.__class__.__name__}.angle : "
                             f"cannot determine the angle of vector (0, 0) !")

        length = magnitude(self.x, self.y)
        __x, __y = vector_from_degree(__angle)
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

    def lerp(self, target, delta: float):
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
        return not approximate_compare(self.x, 0) or not approximate_compare(self.y, 0)

    def __eq__(self, other):
        return approximate_compare(self.x, other.x) and approximate_compare(self.y, other.y)

    def __ne__(self, other):
        return not approximate_compare(self.x, other.x) or not approximate_compare(self.y, other.y)

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

class VectorDependent(Vector):
    """
    - VectorDependent phụ thuộc tương đối vào một Vector khác, nghĩa là
    nó cách một Vector mà nó tham chiếu tới "một khoảng Vector".
    - Nếu nó không được tham chiếu đến Vector khác, mọi hành động đều như Vector thông thường.
    - (*) Sẽ có sai sót nếu chỉ chính nó tham chiếu đến Vector đó.
    """

    def __init__(self, __x, __y):
        super().__init__(__x, __y)
        self.__ref_vector = None

    # Override
    def setxy(self, __x, __y):
        # Không có tham chiếu
        if self.__ref_vector is None:
            Vector.setxy(self, __x, __y)
            return

        # `self` sẽ là "một khoảng Vector"
        # Lấy điểm cần "set" trừ đi `ref_vector`
        Vector.setxy(self, __x - self.__ref_vector.x, __y - self.__ref_vector.y)

    def __event_refvector_changed(self, sender: Vector):
        """ Khi vector tham chiếu thay đổi, chính nó cũng đã thay đổi -> call ``Delegate``

        :param sender: vector tham chiếu ``__ref_vector``"""
        self.delegate.call(self)

    def set_ref(self, __ref_vector: Vector):
        __ref_vector.delegate.add(self, VectorDependent.__event_refvector_changed)
        self.__ref_vector = __ref_vector


    # Override
    @Vector.x.fget
    def x(self):
        __x = Vector.x.fget(self)
        # Không có tham chiếu
        if self.__ref_vector is None:
            return __x
        return self.__ref_vector.x + __x

    # Override
    @Vector.y.fget
    def y(self):
        __y = Vector.y.fget(self)
        # Không có tham chiếu
        if self.__ref_vector is None:
            return __y
        return self.__ref_vector.y + __y
