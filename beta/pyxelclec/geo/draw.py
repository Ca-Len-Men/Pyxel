import numpy as np

from math import e, sqrt, log

def enhance_pixel(pixel_value):
    return round(pixel_value * (2 - pixel_value / 255))

# Tạo mảng alphas là một phần tư hình tròn
def corner(width):
    corner = np.full((width, width), 255, dtype=np.uint8)
    __CONSTANT = (2 ** .5) / 2

    __radius = width - 1
    for j in range(width - 1, (width + 1) // 2 -1, -1):
        for i in range(j, width - j - 1, -1):
            if j < width - 1 and corner[i, j + 1] != 0:
                corner[i, j] = corner[j, i] = 255
                continue

            __distance = (i * i + j * j) ** .5
            __sub = __distance - __radius
            if __sub >= __CONSTANT:
                corner[i, j] = corner[j, i] = 0
            else:
                corner[i, j] = corner[j, i] = enhance_pixel((__CONSTANT - __sub) * 255)

    return corner

# Chỉ thị cho biết bo góc lớn nhất có thể
FULL_BORDER_RADIUS = -1
MAX_ALPHA = 255

def border_alphas_rect(rect_alphas, **kwargs):
    # Keys : border, border_topleft, border_topright, border_bottomleft, border_bottomright
    
    __width, __height = rect_alphas.shape
    __full_width_border = min(__width // 2, __height // 2)

    __border_value = kwargs.get('border')
    if __border_value:
        __width_border = __border_value
        # Chỉ thị bo hết -> gán __width_border bằng __full_width_border
        if __border_value == FULL_BORDER_RADIUS:
            __width_border = __full_width_border
        corner_ = corner(__width_border)
        rect_alphas[0:__width_border, 0:__width_border] = corner_[::-1, ::-1]
        rect_alphas[__width - __width_border:__width, 0:__width_border] = corner_[:, ::-1]
        rect_alphas[0:__width_border, __height - __width_border:__height] = corner_[::-1]
        rect_alphas[__width - __width_border:__width, __height - __width_border:__height] = corner_

        # Nếu tồn tại khóa 'border', các khóa còn lại bị bỏ qua
        return

    # TOP LEFT
    __border_topleft_value = kwargs.get('border_topleft')
    if __border_topleft_value:
        __width_border = __border_topleft_value
        if __border_topleft_value == FULL_BORDER_RADIUS:
            __width_border = __full_width_border

        corner_ = corner(__width_border)
        rect_alphas[0:__width_border, 0:__width_border] = corner_[::-1, ::-1]

    # TOP RIGHT
    __border_topright_value = kwargs.get('border_topright')
    if __border_topright_value:
        __width_border = __border_topright_value
        if __border_topright_value == FULL_BORDER_RADIUS:
            __width_border = __full_width_border

        corner_ = corner(__width_border)
        rect_alphas[__width - __width_border:__width, 0:__width_border] = corner_[:, ::-1]

    # BOTTOM LEFT
    _border_bottomleft_value = kwargs.get('border_bottomleft')
    if _border_bottomleft_value:
        __width_border = _border_bottomleft_value
        if _border_bottomleft_value == FULL_BORDER_RADIUS:
            __width_border = __full_width_border

        corner_ = corner(__width_border)
        rect_alphas[0:__width_border, __height - __width_border:__height] = corner_[::-1]

    # BOTTOM RIGHT
    __border_bottomright_value = kwargs.get('border_bottomright')
    if __border_bottomright_value:
        __width_border = __border_bottomright_value
        if __border_bottomright_value == FULL_BORDER_RADIUS:
            __width_border = __full_width_border

        corner_ = corner(__width_border)
        rect_alphas[__width - __width_border:__width, __height - __width_border:__height] = corner_

def sub_alphas(background, icon, topleft):
    icon_w, icon_h = icon.shape
    background_w, background_h = background.shape

    topleft_x, topleft_y = topleft
    topleft_background_x, topleft_background_y = topleft
    topleft_icon_x, topleft_icon_y = 0, 0

    # icon nằm ngoài background
    if topleft_x >= background_w or topleft_y >= background_h:
        return
    if topleft_x + icon_w <= 0 or topleft_y + icon_h <= 0:
        return

    # bỏ qua những vùng của icon nằm ngoài background
    if topleft_x < 0:
        topleft_background_x = 0
        topleft_icon_x = -topleft_x
        icon_w += topleft_x
    if topleft_y < 0:
        topleft_background_y = 0
        topleft_icon_y = -topleft_y
        icon_h += topleft_y
    if background_w - topleft_background_x < icon_w:
        icon_w = background_w - topleft_background_x
    if background_h - topleft_background_y < icon_h:
        icon_h = background_h - topleft_background_y

    # Hiệu của hai vùng alphas
    background_bounded = background[topleft_background_x:topleft_background_x + icon_w,
                         topleft_background_y:topleft_background_y + icon_h]
    icon_bounded = icon[topleft_icon_x:topleft_icon_x + icon_w,
                        topleft_icon_y:topleft_icon_y + icon_h]
    predicate = background_bounded >= icon_bounded

    background_bounded[predicate] -= icon_bounded[predicate]
    background_bounded[~predicate] = 0

def reflective(canvas_alphas, exp):
    height = canvas_alphas.shape[1]

    for i in range(height):
        row = canvas_alphas[:, i]
        row[:] = (row * pow((1 - i / height), exp)).round()

class CircleGaussian:
    def __init__(self, center_value, radius, radius_value):
        # G(x) = center_value * e^(-x^2 / (2 * sigma^2))
        # center_value = 255
        # Với radius là bán kính hình tròn, tại G(radius) = radius_value, ta có :
        # sigma = sqrt(-radius^2 / (2 * ln(radius_value / center_value)))

        self._center_value = center_value
        self._sigma = sqrt((-radius ** 2) / (2 * log(radius_value/ self._center_value)))

    def gaussian(self, x):
        gaussian_x = self._center_value * e ** (-x ** 2 / (2 * self._sigma ** 2))
        return int(gaussian_x)

def corner_gaussian(width, center_value):
    corner = np.full((width, width), 0, dtype=np.uint8)
    calculater = CircleGaussian(center_value, width - 1, 1)

    for i in range(width):
        for j in range(i, width):
            __x = sqrt(i ** 2 + j ** 2)
            corner[i, j] = corner[j, i] = calculater.gaussian(__x)

    return corner

def gaussian_circle_alpha(circle, center_value):
    diameter = circle.shape[0]
    __width = diameter // 2
    corner = corner_gaussian(__width, center_value)

    circle[0:__width, 0:__width] = corner[::-1, ::-1]
    circle[diameter - __width:diameter, 0:__width] = corner[:, ::-1]
    circle[0:__width, diameter - __width:diameter] = corner[::-1]
    circle[diameter - __width:diameter, diameter - __width:diameter] = corner
