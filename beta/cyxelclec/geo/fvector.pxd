#cython: language_level=3

cimport cython

cdef class Vector:
    cdef double __x
    cdef double __y

    cdef inline double cy_get_x(self):
        return self.__x

    cdef inline void cy_set_x(self, double __x):
        self.cy_setxy(__x, self.__y)

    cdef inline double cy_get_y(self):
        return self.__y

    cdef inline void cy_set_y(self, double __y):
        self.cy_setxy(self.__x, __y)

    cdef inline (double, double) cy_get_tup(self):
        return self.__x, self.__y

    @cython.boundscheck(False)
    @cython.wraparound(False)
    cdef inline void cy_set_tup(self, (double, double) __tup):
        self.cy_setxy(__tup[0], __tup[1])

    cdef inline (int, int) cy_get_tupint(self):
        return <int> self.__x, <int> self.__y

    cdef double cy_get_angle(self)
    cdef void cy_set_angle(self, double __angle)

    cdef void cy_setxy(self, double __x, double __y)
    cdef void cy_set(self, Vector __source)
    cdef bint cy_lerp(self, Vector target, double delta)
    cdef double cy_magnitude(self, Vector other)
    cdef Vector cy_copy(self)
    cdef Vector cy_normalize(self)

    cdef Vector cy_add(self, Vector other)
    cdef Vector cy_iadd(self, Vector other)
    cdef Vector cy_sub(self, Vector other)
    cdef Vector cy_isub(self, Vector other)
    cdef Vector cy_mul_vector(self, Vector other)
    cdef Vector cy_mul_double(self, double value)
    cdef Vector cy_imul_vector(self, Vector other)
    cdef Vector cy_imul_double(self, double value)
    cdef Vector cy_truediv(self, double value)
    cdef Vector cy_itruediv(self, double value)
    cdef Vector cy_floordiv(self, double value)
    cdef Vector cy_ifloordiv(self, double value)
    cdef Vector cy_abs(self)
    cdef bint cy_bool(self)
    cdef bint cy_eq(self, Vector other)
    cdef bint cy_ne(self, Vector other)
    cdef Vector cy_neg(self)
    cdef double cy_float(self)

cdef class WeakrefMethod:
    cdef object __weakref_bounded_method

cdef class Delegate:
    cdef set _weakref_methods

    cdef void cy_add(self, WeakrefMethod __weakref_bounded_method)
    cdef void cy_call(self, tuple args)

cdef class VectorListener(Vector):
    cdef Delegate __delegate

    cdef void cy_add_listener(self, WeakrefMethod __listener)
    cdef void cy_setxy(self, double __x, double __y)
    cdef void cy_only_set(self, Vector __source)