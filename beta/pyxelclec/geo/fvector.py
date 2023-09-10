from .fmath import *

from weakref import WeakMethod
import random

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
    
    def setxy(self, __x, __y):
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
        self.setxy(__x, self.__y)

    @property
    def y(self):
        return self.__y

    @y.setter   # type: ignore
    def y(self, __y):
        self.setxy(self.__x, __y)

    @property
    def angle(self):
        return angle(self.__x, self.__y)

    @angle.setter   # type: ignore
    def angle(self, __angle):
        if relative_compare(self.__x, 0) and relative_compare(self.__y, 0):
            raise ValueError(f"From {self.__class__.__name__}.angle : "
                             f"cannot determine the angle of vector (0, 0) !")

        length = (self.__x * self.__x + self.__y * self.__y) ** .5
        __x, __y = vector(__angle)
        self.setxy(__x * length, __y * length)

    @property
    def tup(self):
        return self.__x, self.__y

    @tup.setter # type: ignore
    def tup(self, __tup):
        self.setxy(*__tup)

    @property
    def tup_int(self):
        return int(self.__x), int(self.__y)

    @tup_int.setter # type: ignore
    def tup_int(self, __tup_int):
        self.setxy(*__tup_int)

    def copy(self):
        return Vector(self.__x, self.__y)

    def magnitude(self, other):
        return distance(self.__x, self.__y, other.x, other.y)

    def normalize(self):
        distance = (self.__x * self.__x + self.__y * self.__y) ** .5
        return Vector(self.__x / distance, self.__y / distance)

    def lerp(self, target, delta):
        __sub = Vector(target.x - self.__x, target.y - self.__y)
        __sub_distance = (__sub.x * __sub.x + __sub.y * __sub.y) ** .5

        if delta > 0 and __sub_distance <= delta:
            self.set(target)
            return True

        __value = delta / __sub_distance
        self.__iadd__(Vector(__sub.x * __value, __sub.y * __value))
        return False

    def __str__(self):
        return f'Vector({self.__x}, {self.__y})'

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return 2

    def __iter__(self):
        yield self.__x
        yield self.__y

    def __copy__(self):
        return self.copy()

    def __add__(self, other):
        return Vector(self.__x + other.x, self.__y + other.y)

    def __iadd__(self, other):
        self.setxy(self.__x + other.x, self.__y + other.y)
        return self

    def __sub__(self, other):
        return Vector(self.__x - other.x, self.__y - other.y)

    def __isub__(self, other):
        self.setxy(self.__x - other.x, self.__y - other.y)
        return self

    def __mul__(self, other):
        if isinstance(other, (Vector, tuple)):
            return Vector(self.__x * other[0], self.__y * other[1])
        elif isinstance(other, (float, int)):
            return Vector(self.__x * other, self.__y * other)

        raise TypeError(f'From {self.__class__.__name__}.__mul__ : '
                        f'type of parameter `other` must be <float, tuple or Vector> !')

    def __imul__(self, other):
        if isinstance(other, (tuple, Vector)):
            self.setxy(self.__x * other[0], self.__y * other[1])
        elif isinstance(other, (int, float)):
            self.setxy(self.__x * other, self.__y * other)
        else:
            raise TypeError(f'From {self.__class__.__name__}.__imul__ : '
                            f'type of parameter `other` must be <float, tuple, Vector> !')
        return self

    def __truediv__(self, val):
        return Vector(self.__x / val, self.__y / val)

    def __itruediv__(self, val):
        self.setxy(self.__x / val, self.__y / val)
        return self

    def __floordiv__(self, val):
        return Vector(self.__x // val, self.__y // val)

    def __ifloordiv__(self, val):
        self.setxy(self.__x // val, self.__y // val)
        return self

    def __abs__(self):
        return Vector(abs(self.__x), abs(self.__y))

    def __bool__(self):
        return not relative_compare(self.__x, 0) or not relative_compare(self.__y, 0)

    def __eq__(self, other):
        return relative_compare(self.__x, other.x) and relative_compare(self.__y, other.y)

    def __ne__(self, other):
        return not relative_compare(self.__x, other.x) or not relative_compare(self.__y, other.y)

    def __neg__(self):
        return Vector(-self.__x, -self.__y)

    def __float__(self):
        return (self.__x * self.__x + self.__y * self.__y) ** .5

    def __getitem__(self, i):
        if i == 0:
            return self.__x
        elif i == 1:
            return self.__y
        else:
            raise IndexError(f"From {self.__class__.__name__}.__getitem__ : "
                             f"Vector index out of range !")

    def __setitem__(self, i, value):
        if i == 0:
            self.setxy(value, self.__y)
        elif i == 1:
            self.setxy(self.__x, value)
        else:
            raise IndexError(f"From {self.__class__.__name__}.__getitem__ : "
                             f"Vector index out of range !")

class WeakrefMethod:
    def __init__(self, __bounded_method):
        self.__weakref_bounded_method = WeakMethod(__bounded_method)

    def __call__(self, *args):
        __callable = self.__weakref_bounded_method()
        if __callable:
            __callable(*args)
        return __callable is not None

class Delegate:
    def __init__(self):
        self._weakref_methods = None    # type: ignore

    def call(self, *args):
        if self._weakref_methods is None:
            return

        recycle_bin = None
        for __callable in self._weakref_methods:    # type: ignore
            result = __callable(*args)
            if not result:
                if recycle_bin is None:
                    recycle_bin = set()
                recycle_bin.add(__callable)
                
        if recycle_bin:
            self._weakref_methods -= recycle_bin

    def add(self, __weakref_bounded_method):
        # assert isinstance(__weakref_bounded_method, WeakrefMethod), \
        #     f"From {self.__class__.__name__}.add : " \
        #     f"parameter type of '__weakref_bounded_method' must be <WeakrefMethod> !"
        
        if self._weakref_methods is None:
            self._weakref_methods = set()
        self._weakref_methods.add(__weakref_bounded_method)

class VectorListener(Vector):
    def __init__(self, __x, __y):
        super().__init__(__x, __y)
        self.__delegate = Delegate()

    def add_listener(self, __listener):
        self.__delegate.add(__listener)

    def setxy(self, __x, __y):
        super().setxy(__x, __y)
        self.__delegate.call(self.copy())

    def only_set(self, source):
        super().setxy(*source)
