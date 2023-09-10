#cython: language_level=3

cdef double cy_angle(double vec_x, double vec_y):
    cdef double degrees = cy_degrees(atan2(vec_y, vec_x))
    return degrees + 360 if degrees < 0 else degrees

cdef (double, double) cy_vector(double degrees):
    degrees %= 360
    if degrees < 0:
        degrees += 360

    cdef:
        double y = sin(cy_radians(degrees))
        double x = sqrt(1 - y * y)
    return (-x, y) if 90 < degrees < 270 else (x, y)

cdef double cy_lerp(double current, double target, double delta):
    if delta > 0:
        if fabs(current - target) <= delta:
            return target
    return current + delta if current < target else current - delta
