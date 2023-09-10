#cython: language_level=3

import numpy as np
cimport numpy as np

import pygame

#TODO     =====     Pure Python     =====

keys_border_radius = {'border', 'border_topleft', 'border_topright',
                      'border_bottomleft', 'border_bottomright'}

def scale_pixels(grid_pixel, size):
    source = np.array(grid_pixel)
    if source.shape[2] == 4:
        source = source[:, :, :3]

    surface = pygame.surfarray.make_surface(np.swapaxes(source, 0, 1))
    return pygame.transform.smoothscale(surface, size)

def new_surface(size, color=Color.NoColor):
    surface = pygame.Surface(size, pygame.SRCALPHA)
    surface.fill(color)
    return surface

def add_padding(surface, width, color=Color.NoColor):
    """``Method`` **surface_padding** : copy new image have padding.

    - If **width** is type ``int`` : default left, right, top, bottom padding is **width**.
    - If **width** is type ``Tuple[int, int, int, int]`` : the padding values in order are left, right, top, bottom.

    :param surface: image
    :type surface: pygame.Surface
    :param width: padding width
    :type width: int | Tuple[int, int, int, int]
    :param color: padding color
    :return: new image
    """

    size = surface.get_size()
    if isinstance(width, int):
        bg = new_surface((size[0] + width * 2, size[1] + width * 2), color)
        bg.blit(surface, (width, width))
    elif isinstance(width, tuple):
        bg = new_surface((size[0] + width[0] + width[1], size[1] + width[2] + width[3]), color)
        bg.blit(surface, (width[0], width[2]))
    else:
        raise TypeError(f'From add_padding : '
                        f'type of parameter `width` must be <int, tuple> !')
    return bg

def rect(size, color, **kwargs):
    """``Method`` **rect** : drawing rectangle and return the new image.

    - Keys : border, border_topleft, border_topright, border_bottomleft, border_bottomright
    """

    __surface = new_surface(size, color)
    cdef np.ndarray[UINT8_t, ndim=2] __pixels = pygame.surfarray.pixels_alpha(__surface)
    cy_border_alphas_rect(__pixels, kwargs)
    return __surface

def rect_width(size, color, int width, **kwargs):
    cdef:
        np.ndarray[UINT8_t, ndim=2] __rect_alphas, __rect_inside_alphas
        Vector __size_rect_inside

    __rect = rect(size, color, kwargs)
    __rect_alphas = pygame.surfarray.pixels_alpha(__rect)
    cy_border_alphas_rect(__rect_alphas, kwargs)

    __size_rect_inside = Vector(size[0] - 2 * width, size[1] - 2 * width)
    __rect_inside_alphas = np.full(__size_rect_inside.cy_get_tupint(), 255, dtype=np.uint8)
    cy_border_alphas_rect(__rect_inside_alphas, kwargs)

    cy_sub_alphas(__rect_alphas, __rect_inside_alphas, width, width)
    return __rect

def circle(edge, color):
    """``Method`` **circle** : drawing circle and return new image."""

    surface = new_surface((edge, edge), color)
    cdef np.ndarray[UINT8_t, ndim=2] __pixels = pygame.surfarray.pixels_alpha(surface)
    cy_border_alphas_rect(__pixels, {'border': <int>(edge / 2)})
    return surface

def gaussian_circle(edge, color):
    surface = new_surface((edge, edge), color)
    cdef np.ndarray[UINT8_t, ndim=2] __pixels = pygame.surfarray.pixels_alpha(surface)
    cy_gaussian_circle_alpha(__pixels, color[3])
    return surface

def fill_mask(surface, color):
    cdef:
        np.ndarray[UINT8_t, ndim=2] alphas_of_surface, alphas_of_full_surface

    alphas_of_surface = pygame.surfarray.pixels_alpha(surface)

    result_surface = new_surface(surface.get_size(), color)
    alphas_of_full_surface = pygame.surfarray.pixels_alpha(result_surface)
    alphas_of_full_surface[:] = (alphas_of_surface * (color[3] / 255)).round()
    return result_surface


def insert_to_square(surface, centroid=Vector.zero()):
    """``Method`` **square** : create square image from **surface**,
    with center of square is **centroid** point in **surface**.

    :param surface: image
    :type surface: pygame.Surface
    :param centroid: point in surface
    :return: square image
    """
    cdef:
        Vector centroid_vector
        int edge
        (int, int) size

    size = surface.get_size()
    centroid_vector = Vector(size[0] / 2 + centroid[0], size[1] / 2 + centroid[1])
    x1, x2 = abs(centroid_vector.cy_get_x()), abs(centroid_vector.cy_get_x() - size[0])
    y1, y2 = abs(centroid_vector.cy_get_y()), abs(centroid_vector.cy_get_y() - size[1])
    edge = <int>max(x1, x2, y1, y2)

    result_surface = new_surface((edge * 2, edge * 2))
    result_surface.blit(surface, Vector(edge, edge).cy_sub(centroid_vector))
    return result_surface

def enhancement(surface):
    cdef np.ndarray[UINT8_t, ndim=2] source

    source = pygame.surfarray.pixels_alpha(surface)
    source[:] = (source * (2 - source / 255)).round()

def linear_gradient_icon(surface, grid_pixel):
    cdef:
        np.ndarray[UINT8_t, ndim=2] surface_alphas, predicate
        np.ndarray[UINT8_t, ndim=3] linear_gradient_colors, surface_colors

    linear_gradient = scale_pixels(grid_pixel, surface.get_size())
    linear_gradient_colors = pygame.surfarray.pixels3d(linear_gradient)
    surface_colors = pygame.surfarray.pixels3d(surface)
    surface_alphas = pygame.surfarray.pixels_alpha(surface)

    predicate = surface_alphas != 0
    surface_colors[predicate] = linear_gradient_colors[predicate]

def border_corner(surface, **kwargs):
    cdef:
        np.ndarray[UINT8_t, ndim=2] alphas_surf

    surface_alphas = pygame.surfarray.pixels_alpha(surface)
    cy_border_alphas_rect(surface_alphas, kwargs)
