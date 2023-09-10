#cython: language_level=3


from . cimport fmath
from .fmath cimport *

cimport cython
from weakref import WeakMethod
import random

cdef class Vector:
    def __cinit__(self, double __x, double __y):
        self.__x = __x
        self.__y = __y
    
    # Những thay đổi trên x, y của Vector luôn phải gọi hàm này
    cdef void cy_setxy(self, double __x, double __y):
        self.__x = __x
        self.__y = __y

    cdef void cy_set(self, Vector __source):
        self.cy_setxy(__source.__x, __source.__y)

    cdef Vector cy_copy(self):
        return Vector(self.__x, self.__y)

    cdef double cy_magnitude(self, Vector other):
        return cy_magnitude(self.__x - other.__x, self.__y - other.__y)

    @cython.cdivision(True)
    cdef Vector cy_normalize(self):
        cdef double __length = cy_magnitude(self.__x, self.__y)
        return Vector(self.__x / __length, self.__y / __length)

    @cython.cdivision(True)
    cdef bint cy_lerp(self, Vector target, double delta):
        cdef:
            Vector __sub
            double __sub_length, __value

        __sub = Vector(target.__x - self.__x, target.__y - self.__y)
        __sub_length = cy_magnitude(__sub.__x, __sub.__y)

        if delta > 0 and __sub_length <= delta:
            self.cy_set(target)
            return True

        __value = delta / __sub_length
        self.cy_setxy(self.__x + __sub.__x * __value, self.__y + __sub.__y * __value)
        return False

    cdef double cy_get_angle(self):
        return cy_angle(self.__x, self.__y)

    cdef void cy_set_angle(self, double __angle):
        if cy_compare(self.__x, 0) and cy_compare(self.__y, 0):
            raise ValueError(f"From {self.__class__.__name__}.angle : "
                             f"cannot determine the angle of vector (0, 0) !")

        cdef:
            double __x, __y, __length

        __length = cy_magnitude(self.__x, self.__y)
        __x, __y = cy_vector(__angle)
        self.cy_setxy(__x * __length, __y * __length)

    cdef Vector cy_add(self, Vector other):
        return Vector(self.__x + other.__x, self.__y + other.__y)

    cdef Vector cy_iadd(self, Vector other):
        self.cy_setxy(self.__x + other.__x, self.__y + other.__y)
        return self

    cdef Vector cy_sub(self, Vector other):
        return Vector(self.__x - other.__x, self.__y - other.__y)

    cdef Vector cy_isub(self, Vector other):
        self.cy_setxy(self.__x - other.__x, self.__y - other.__y)
        return self

    cdef Vector cy_mul_vector(self, Vector other):
        return Vector(self.__x * other.__x, self.__y * other.__y)

    cdef Vector cy_mul_double(self, double value):
        return Vector(self.__x * value, self.__y * value)

    cdef Vector cy_imul_vector(self, Vector other):
        self.cy_setxy(self.__x * other.__x, self.__y * other.__y)
        return self

    cdef Vector cy_imul_double(self, double value):
        self.cy_setxy(self.__x * value, self.__y * value)
        return self

    @cython.cdivision(True)
    cdef Vector cy_truediv(self, double value):
        return Vector(self.__x / value, self.__y / value)

    @cython.cdivision(True)
    cdef Vector cy_itruediv(self, double value):
        self.cy_setxy(self.__x / value, self.__y / value)
        return self

    @cython.cdivision(True)
    cdef Vector cy_floordiv(self, double value):
        return Vector(<int>(self.__x / value), <int>(self.__y // value))

    @cython.cdivision(True)
    cdef Vector cy_ifloordiv(self, double value):
        self.cy_setxy(<int>(self.__x / value), <int>(self.__y / value))
        return self

    cdef Vector cy_abs(self):
        return Vector(fabs(self.__x), fabs(self.__y))

    cdef bint cy_bool(self):
        return not cy_compare(self.__x, 0) or not cy_compare(self.__y, 0)

    cdef bint cy_eq(self, Vector other):
        return cy_compare(self.__x, other.__x) and cy_compare(self.__y, other.__y)

    cdef bint cy_ne(self, Vector other):
        return not cy_compare(self.__x, other.__x) or not cy_compare(self.__y, other.__y)

    cdef Vector cy_neg(self):
        return Vector(-self.__x, -self.__y)

    cdef double cy_float(self):
        return cy_magnitude(self.__x, self.__y)

    #   =====     Pure Python     =====

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
        cdef double x, y
        x = random.random()
        y = 1 - x * x
        return cls(x, y) if random.randint(0, 1) else cls(x, -y)

    def setxy(self, double __x, double __y):
        self.__x = __x
        self.__y = __y

    def set(self, source):
        cdef Vector __source

        if isinstance(source, Vector):
            __source = <Vector>source
            self.setxy(__source.__x, __source.__y)
        elif isinstance(source, (tuple, list)):
            self.setxy(*source)
        else:
            raise TypeError(f'From {self.__class__.__name__}.set : '
                            f'parameter type `source` must be <tuple, list, Vector> !')

    @property
    def x(self):
        return self.__x

    @x.setter   # type: ignore
    def x(self, double __x):
        self.setxy(__x, self.__y)

    @property
    def y(self):
        return self.__y

    @y.setter   # type: ignore
    def y(self, double __y):
        self.setxy(self.__x, __y)

    @property
    def angle(self):
        return self.cy_get_angle()

    @angle.setter   # type: ignore
    def angle(self, double __angle):
        if cy_compare(self.__x, 0) and cy_compare(self.__y, 0):
            raise ValueError(f"From {self.__class__.__name__}.angle : "
                             f"cannot determine the angle of vector (0, 0) !")

        cdef:
            double __x, __y, __length

        __length = cy_magnitude(self.__x, self.__y)
        __x, __y = cy_vector(__angle)
        self.setxy(__x * __length, __y * __length)

    @property
    def tup(self):
        return self.__x, self.__y

    @cython.boundscheck(False)
    @cython.wraparound(False)
    @tup.setter # type: ignore
    def tup(self, (double, double) __tup):
        self.setxy(__tup[0], __tup[1])

    @property
    def tup_int(self):
        return <int>self.__x, <int>self.__y

    def copy(self):
        return self.cy_copy()

    def magnitude(self, other):
        return cy_magnitude(self.__x - other.x, self.__y - other.y)

    def normalize(self):
        return self.cy_normalize()

    @cython.cdivision(True)
    def lerp(self, Vector target, double delta):
        cdef:
            Vector __sub = Vector(target.__x - self.__x, target.__y - self.__y)
            double __sub_distance = cy_magnitude(__sub.__x, __sub.__y)
            double __value

        if delta > 0 and __sub_distance <= delta:
            self.setxy(target.__x, target.__y)
            return True

        __value = delta / __sub_distance
        self.setxy(self.__x + __sub.__x * __value, self.__y + __sub.__y * __value)
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

    def __add__(self, Vector other):
        return self.cy_add(other)

    def __iadd__(self, Vector other):
        self.setxy(self.__x + other.__x, self.__y + other.__y)
        return self

    def __sub__(self, Vector other):
        return self.cy_sub(other)

    def __isub__(self, Vector other):
        self.setxy(self.__x - other.__x, self.__y - other.__y)
        return self

    @cython.boundscheck(False)
    @cython.wraparound(False)
    def __mul__(self, other):
        cdef:
            Vector __other_is_vector

        if isinstance(other, Vector):
            __other_is_vector = <Vector> other
            return self.cy_mul_vector(__other_is_vector)
        elif isinstance(other, tuple):
            return Vector(self.__x * <double>other[0], self.__y * <double>other[1])
        elif isinstance(other, (float, int)):
            return self.cy_mul_double(other)

        raise TypeError(f'From {self.__class__.__name__}.__mul__ : '
                        f'type of parameter `other` must be <float, tuple or Vector> !')

    @cython.boundscheck(False)
    @cython.wraparound(False)
    def __imul__(self, other):
        cdef:
            Vector __other_is_vector
            double __other_is_double

        if isinstance(other, Vector):
            __other_is_vector = <Vector> other
            self.setxy(self.__x * __other_is_vector.__x, self.__y * __other_is_vector.__y)
        if isinstance(other, tuple):
            self.setxy(self.__x * other[0], self.__y * other[1])
        elif isinstance(other, (int, float)):
            __other_is_double = <double> other
            self.setxy(self.__x * __other_is_double, self.__y * __other_is_double)
        else:
            raise TypeError(f'From {self.__class__.__name__}.__imul__ : '
                            f'type of parameter `other` must be <float, tuple, Vector> !')
        return self

    def __truediv__(self, double value):
        return self.cy_truediv(value)

    def __itruediv__(self, double value):
        self.setxy(self.__x / value, self.__y / value)
        return self

    def __floordiv__(self, double value):
        return self.cy_floordiv(value)

    def __ifloordiv__(self, double value):
        self.setxy(<int>(self.__x / value), <int>(self.__y / value))
        return self

    def __abs__(self):
        return self.cy_abs()

    def __bool__(self):
        return self.cy_bool()

    def __eq__(self, Vector other):
        return self.cy_eq(other)

    def __ne__(self, Vector other):
        return self.cy_ne(other)

    def __neg__(self):
        return self.cy_neg()

    def __float__(self):
        return cy_magnitude(self.__x, self.__y)

    def __getitem__(self, int i):
        if i == 0:
            return self.__x
        elif i == 1:
            return self.__y
        else:
            raise IndexError(f"From {self.__class__.__name__}.__getitem__ : "
                             f"Vector index out of range !")

    def __setitem__(self, int i, double value):
        if i == 0:
            self.setxy(value, self.__y)
        elif i == 1:
            self.setxy(self.__x, value)
        else:
            raise IndexError(f"From {self.__class__.__name__}.__getitem__ : "
                             f"Vector index out of range !")

cdef class WeakrefMethod:
    def __init__(self, __bounded_method):
        self.__weakref_bounded_method = WeakMethod(__bounded_method)

    def __call__(self, *args):
        __callable = self.__weakref_bounded_method()
        if __callable:
            __callable(*args)
        return __callable is not None

cdef class Delegate:
    #TODO     =====     Cython     =====

    cdef void cy_add(self, WeakrefMethod __weakref_bounded_method):
        if self._weakref_methods is None:
            self._weakref_methods = set()
        self._weakref_methods.add(__weakref_bounded_method)

    cdef void cy_call(self, tuple args):
        if self._weakref_methods is None:
            return

        cdef set recycle_bin = None
        for __callable in self._weakref_methods:    # type: ignore
            result = __callable(*args)
            if not result:
                if recycle_bin is None:
                    recycle_bin = set()
                recycle_bin.add(__callable)

        if recycle_bin:
            self._weakref_methods -= recycle_bin

    #TODO     =====     Pure Python     =====

    def __init__(self):
        self._weakref_methods = None

    def add(self, WeakrefMethod __weakref_bounded_method):
        self.cy_add(__weakref_bounded_method)

    def call(self, *args):
        self.cy_call(args)

cdef class VectorListener(Vector):
    #TODO     =====     Cython     =====

    cdef void cy_add_listener(self, WeakrefMethod __listener):
        self.__delegate.cy_add(__listener)

    cdef void cy_setxy(self, double __x, double __y):
        Vector.cy_setxy(self, __x, __y)
        self.__delegate.cy_call((self.cy_copy(),))

    cdef void cy_only_set(self, Vector __source):
        Vector.cy_set(self, __source)

    #TODO     =====     Pure Python     =====

    def __init__(self, double __x, double __y):
        Vector.__init__(self, __x, __y)
        self.__delegate = Delegate()

    def add_listener(self, __listener):
        self.__delegate.add(__listener)

    def setxy(self, double __x, double __y):
        Vector.setxy(self, __x, __y)
        self.__delegate.call(self.cy_copy())

    def only_set(self, source):
        Vector.cy_set(self, source)
