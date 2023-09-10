
from math import atan2, sin

E = 0.000000001
PI = 3.14159_26535_89793

def _radians(degree):
     return degree * PI / 180

def _degrees(radian):
    return radian * (180 / PI)

# ==================================================

def relative_compare(a, b):
    return abs(a - b) <= E

def angle(vec_x, vec_y):
    degrees = _degrees(atan2(vec_y, vec_x))
    return degrees + 360 if degrees < 0 else degrees

def vector(degrees):
    degrees %= 360
    if degrees < 0:
        degrees += 360

    y = sin(_radians(degrees))
    x = (1 - y * y) ** .5
    return (-x, y) if 90 < degrees < 270 else (x, y)

def distance(a_x, a_y, b_x, b_y):
    sub_x = a_x - b_x
    sub_y = a_y - b_y
    return (sub_x * sub_x + sub_y * sub_y) ** .5

def lerp(current, target, delta):
    if delta > 0:
        if abs(current - target) <= delta:
            return target
    return current + delta if current < target else current - delta
