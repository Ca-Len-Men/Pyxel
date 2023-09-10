#cython: language_level=3

cdef extern from *:
    """
    #include <math.h>

    const double cy_approximate = 0.000000001;
    const double cy_pi = 3.141592653589793;
    const double cy_e = 2.718281828459045;

    #define cy_min(x, y)  ( (x) < (y) ? (x) : (y) )
    #define cy_max(x, y)  ( (x) > (y) ? (x) : (y) )
    #define cy_sqr_magnitude(x, y)  ( (x) * (x) + (y) * (y) )
    #define cy_magnitude(x, y)  ( sqrt(cy_sqr_magnitude(x, y)) )

    double cy_radians(double degrees) {
        return degrees * cy_pi / 180;
    }

    double cy_degrees(double radians) {
        return radians * (180 / cy_pi);
    }
    """

    # <math.h> define
    cdef double ceil(double x)
    cdef double sqrt(double x)
    cdef double cpow "pow"(double a, double x)
    cdef double fabs(double x)
    cdef double log(double x)
    cdef double sin(double x)
    cdef double atan2(double x, double y)

    # Cython define
    cdef double cy_approximate
    cdef double cy_pi
    cdef double cy_e

    cdef double cy_radians(double degrees)
    cdef double cy_degrees(double radians)
    cdef double cy_min(double x, double y)
    cdef double cy_max(double x, double y)
    cdef double cy_sqr_magnitude(double x, double y)
    cdef double cy_magnitude(double x, double y)

# ==================================================

cdef inline bint cy_compare(double a, double b):
    return fabs(a - b) < cy_approximate

cdef double cy_angle(double vec_x, double vec_y)
cdef (double, double) cy_vector(double degrees)
cdef double cy_lerp(double current, double target, double delta)


