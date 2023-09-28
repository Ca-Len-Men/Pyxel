# /**************************************************************************/
# /*  pmath.py                                                              */
# /**************************************************************************/
# /*                         This file is part of:                          */
# /*                                 PYXEL                                  */
# /*                  https://github.com/Ca-Len-Men/Pyxel                   */
# /**************************************************************************/

from math import atan2, sin, sqrt, pi
from typing import *

APPROXIMATE = 0.000000001
PI = pi # 3.14159_26535_89793

def _degree_to_radian(__degrees: float):
     return __degrees * PI / 180

def _radian_to_degree(__radians: float):
    return __radians * (180 / PI)

# /**************************************************************************/

def magnitude(x: float, y: float) -> float:
    """:return: **sqrt(x * x + y * y)**"""
    return sqrt(x * x + y * y)

def approximate_compare(a: float, b: float) -> bool:
    """ *So sánh gần đúng* hai giá trị kiểu ``float``.
    :return: True nếu **abs(a - b) <= APPROXIMATE**
    """
    return abs(a - b) <= APPROXIMATE

def angle_of_vector(vec_x: float, vec_y: float) -> float:
    """ Tính góc của **vector(vec_x, vec_y)**.
    :return: góc của vector ( **degree** ) - trong đoạn **[0, 360]**
    """
    degree = _radian_to_degree(atan2(vec_y, vec_x))
    # Tăng 360 nếu góc là âm
    return degree + 360 if degree < 0 else degree

def vector_from_degree(__degree: float) -> Tuple[float, float]:
    """ Tạo vector có độ dài **1** từ một góc **__degree**.
    :return: vector có độ dài **1**
    """

    __degree %= 360
    if __degree < 0:
        __degree += 360

    y = sin(_degree_to_radian(__degree))
    x = (1 - y * y) ** .5
    return (-x, y) if 90 < __degree < 270 else (x, y)

def lerp_float(current: float, target: float, delta: float) -> float:
    """ Từ giá trị **current**, tịnh tiến một đoạn **delta** đến giá trị **target**.

    - **(!)** : khi **delta** *âm*, tịnh tiến *hướng ngược lại* với **target**.
    :return: giá trị sau khi tịnh tiến
    """

    if delta > 0:
        # <delta> dương và khoảng cách đến <target> bé hơn <delta>
        # -> Trả về <target>
        if abs(current - target) <= delta:
            return target

    # Nếu <current> nằm bên trái <target> trên trục Ox
    # -> current + delta
    #  ngược lại <current> nằm bên phải <target>
    # -> current - delta
    return current + delta if current < target else current - delta
