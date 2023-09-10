#cython: language_level=3

from . cimport fmath
from .fmath cimport *

cimport cython
import numpy as np
cimport numpy as np

ctypedef np.uint8_t UINT8_t

# Chỉ thị cho biết bo góc lớn nhất có thể
cdef int FULL_BORDER_RADIUS = -1

# Tăng cường alpha
cdef inline UINT8_t cy_enhance_pixel(double alpha_value):
    return <UINT8_t> ceil(alpha_value * (2 - alpha_value / 255))

cdef np.ndarray[UINT8_t, ndim=2] cy_corner(int edge)

cdef void cy_border_alphas_rect(
    np.ndarray[UINT8_t, ndim=2] rect_alphas, dict kwargs
)

cdef void cy_sub_alphas(
    np.ndarray[UINT8_t, ndim = 2] background,
    np.ndarray[UINT8_t, ndim = 2] icon,
    int topleft_x, int topleft_y
)

#                   ===== Gaussian =====

cdef extern from *:
    """
    #include <math.h>
    #include <stdlib.h>

    struct CyCircleGaussian {
        double center_value;
        double sigma;
    };

    void init_CyCircleGaussian(struct CyCircleGaussian* pointer,
                double center_value, double radius, double radius_value) {
        pointer->center_value = center_value;
        pointer->sigma = sqrt((-radius * radius) / (2 * log(radius_value / center_value)));
    }

    struct CyCircleGaussian* new_CyCircleGaussian(double center_value, double radius, double radius_value) {
        struct CyCircleGaussian* pointer = 0;
        pointer = (struct CyCircleGaussian*) malloc(sizeof(struct CyCircleGaussian));

        init_CyCircleGaussian(pointer, center_value, radius, radius_value);
        return pointer;
    }

    void del_CyCircleGaussian(struct CyCircleGaussian* pointer) {
        free(pointer);
    }

    double gaussian(struct CyCircleGaussian* pointer, double x) {
        double gaussian_x = pointer->center_value *
                         exp(-x * x / (2 * pointer->sigma * pointer->sigma));
        return gaussian_x;
    }

    """

    # G(x) = center_value * e^(-x^2 / (2 * sigma^2))
    # center_value = 255
    # Với radius là bán kính hình tròn, tại G(radius) = radius_value, ta có :
    # sigma = sqrt(-radius^2 / (2 * ln(radius_value / center_value)))

    cdef struct CyCircleGaussian:
        double center_value
        double sigma

    cdef CyCircleGaussian* new_CyCircleGaussian(double center_value, double radius, double radius_value)
    cdef void del_CyCircleGaussian(CyCircleGaussian* pointer)
    cdef double gaussian(CyCircleGaussian* pointer, double x)

cdef np.ndarray[UINT8_t, ndim=2] cy_corner_gaussian(int width, int center_value)

cdef void cy_gaussian_circle_alpha(
    np.ndarray[UINT8_t, ndim=2] circle,
    int center_value
)
