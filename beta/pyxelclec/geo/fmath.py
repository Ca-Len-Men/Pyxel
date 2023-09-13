
from math import atan2, sin

APPROXIMATE = 0.000000001
PI = 3.14159_26535_89793

def _radians(__degrees):
     return __degrees * PI / 180

def _degrees(__radians):
    return __radians * (180 / PI)

# ==================================================

def relative_compare(a, b):
    return abs(a - b) <= APPROXIMATE

def angle(vec_x, vec_y):
    degrees = _degrees(atan2(vec_y, vec_x))
    return degrees + 360 if degrees < 0 else degrees

def vector(__degrees):
    __degrees %= 360
    if __degrees < 0:
        __degrees += 360

    y = sin(_radians(__degrees))
    x = (1 - y * y) ** .5
    return (-x, y) if 90 < __degrees < 270 else (x, y)

def magnitude(x, y):
    return (x ** 2 + y ** 2) ** .5

def lerp(current, target, delta):
    if delta > 0:
        if abs(current - target) <= delta:
            return target
    return current + delta if current < target else current - delta
