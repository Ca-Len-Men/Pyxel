#cython: language_level=3

cimport cython

#TODO     =====     Cython     =====

# Tạo mảng alphas là một phần tư hình tròn ( bán kính = edge )
@cython.boundscheck(False)
@cython.wraparound(False)
cdef np.ndarray[UINT8_t, ndim=2] cy_corner(int edge):
    cdef:
        np.ndarray[UINT8_t, ndim=2] _corner = np.full((edge, edge), 255, dtype=np.uint8)
        double __CONSTANT = sqrt(2) / 2
        int __radius = edge - 1

        # Khai báo biến tạm
        int i, j
        double __magnitude
        double __sub        # Hiệu của `khoảng cách` và bán kính đường tròn

    for j in range(edge - 1, <int>((edge + 1) / 2) - 1, -1):
        for i in range(j, edge - j - 1, -1):
            if j < edge - 1 and _corner[i, j + 1] != 0:
                _corner[i, j] = _corner[j, i] = 255
                continue

            __magnitude = cy_magnitude(i, j)

            __sub = __magnitude - __radius
            if __sub >= __CONSTANT:
                _corner[i, j] = _corner[j, i] = 0
            else:
                _corner[i, j] = _corner[j, i] = cy_enhance_pixel((__CONSTANT - __sub) * 255)

    return _corner

# Nhận vào một hình chữ nhật alphas và bo góc nó
@cython.boundscheck(False)
@cython.wraparound(False)
cdef void cy_border_alphas_rect(
    np.ndarray[UINT8_t, ndim=2] rect_alphas, dict kwargs
):
    # Các khóa được sử dụng :
    # 'border': bo bốn góc của hình chữ nhật, nếu tồn tại khóa này, các khóa khác bị bỏ qua
    # 'border_topleft', 'border_topright', 'border_bottomleft', 'border_bottomright'

    cdef:
        Py_ssize_t __width = rect_alphas.shape[0]     # type: ignore
        Py_ssize_t __height = rect_alphas.shape[1]    # type: ignore
        int __full_border = <int> cy_min(<int>(__width / 2), <int>(__height / 2))

        # Khai báo biến tạm
        int __edge_border
        np.ndarray[UINT8_t, ndim = 2] _corner

    __border = kwargs.get('border')
    if __border is not None:
        __edge_border = __border
        # Chỉ thị bo hết -> gán __edge_border bằng __full_border
        if __edge_border == FULL_BORDER_RADIUS:
            __edge_border = __full_border

        _corner = cy_corner(__edge_border)
        rect_alphas[0:__edge_border, 0:__edge_border] = _corner[::-1, ::-1]
        rect_alphas[__width - __edge_border:__width, 0:__edge_border] = _corner[:, ::-1]
        rect_alphas[0:__edge_border, __height - __edge_border:__height] = _corner[::-1]
        rect_alphas[__width - __edge_border:__width, __height - __edge_border:__height] = _corner

        # Nếu tồn tại khóa 'border', các khóa còn lại bị bỏ qua
        return

    # TOP LEFT
    __border_topleft = kwargs.get('border_topleft')
    if __border_topleft is not None:
        __edge_border = __border_topleft
        if __edge_border == FULL_BORDER_RADIUS:
            __edge_border = __full_border

        _corner = cy_corner(__edge_border)
        rect_alphas[0:__edge_border, 0:__edge_border] = _corner[::-1, ::-1]

    # TOP RIGHT
    __border_topright = kwargs.get('border_topright')
    if __border_topright is not None:
        __edge_border = __border_topright
        if __edge_border == FULL_BORDER_RADIUS:
            __edge_border = __full_border

        _corner = cy_corner(__edge_border)
        rect_alphas[__width - __edge_border:__width, 0:__edge_border] = _corner[:, ::-1]

    # BOTTOM LEFT
    __border_bottomleft = kwargs.get('border_bottomleft')
    if __border_bottomleft is not None:
        __edge_border = __border_bottomleft
        if __edge_border == FULL_BORDER_RADIUS:
            __edge_border = __full_border

        _corner = cy_corner(__edge_border)
        rect_alphas[0:__edge_border, __height - __edge_border:__height] = _corner[::-1]

    # BOTTOM RIGHT
    __border_bottomright = kwargs.get('border_bottomright')
    if __border_bottomright != 0:
        __edge_border = __border_bottomright
        if __edge_border == FULL_BORDER_RADIUS:
            __edge_border = __full_border

        _corner = cy_corner(__edge_border)
        rect_alphas[__width - __edge_border:__width, __height - __edge_border:__height] = _corner

@cython.boundscheck(False)
@cython.wraparound(False)
cdef void cy_sub_alphas(
    np.ndarray[UINT8_t, ndim = 2] background,
    np.ndarray[UINT8_t, ndim = 2] icon,
    int topleft_x, int topleft_y
):
    cdef:
        Py_ssize_t icon_w = icon.shape[0]              # type: ignore
        Py_ssize_t icon_h = icon.shape[1]              # type: ignore
        Py_ssize_t background_w = background.shape[0]  # type: ignore
        Py_ssize_t background_h = background.shape[1]  # type: ignore

        np.ndarray[UINT8_t, ndim = 2] background_bounded, icon_bounded, predicate
        int topleft_background_x = topleft_x
        int topleft_background_y = topleft_y
        int topleft_icon_x = 0, topleft_icon_y = 0

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
    if background_w - topleft_background_x < icon_w :
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

@cython.boundscheck(False)
@cython.wraparound(False)
cdef np.ndarray[UINT8_t, ndim=2] \
        cy_corner_gaussian(int width, int center_value):
    cdef:
        np.ndarray[UINT8_t, ndim=2] _corner = np.full((width, width), 0, dtype=np.uint8)
        CyCircleGaussian* calculater = new_CyCircleGaussian(center_value, width - 1, 1)

        # Khai báo biến tạm
        int i, j
        double __x

    for i in range(width):
        for j in range(i, width):
            __x = cy_magnitude(i, j)
            _corner[i, j] = _corner[j, i] = <UINT8_t>gaussian(calculater, __x)

    del_CyCircleGaussian(calculater)
    return _corner

@cython.boundscheck(False)
@cython.wraparound(False)
cdef void cy_gaussian_circle_alpha(
    np.ndarray[UINT8_t, ndim=2] circle,
    int center_value
):
    cdef:
        Py_ssize_t diameter = circle.shape[0]   # type: ignore
        Py_ssize_t _width = <Py_ssize_t>(diameter / 2)
        np.ndarray[UINT8_t, ndim=2] _corner = cy_corner_gaussian(_width, center_value)

    circle[0:_width, 0:_width] = _corner[::-1, ::-1]
    circle[diameter - _width:diameter, 0:_width] = _corner[:, ::-1]
    circle[0:_width, diameter - _width:diameter] = _corner[::-1]
    circle[diameter - _width:diameter, diameter - _width:diameter] = _corner

#TODO     =====     Pure Python     =====


