# /**************************************************************************/
# /*  processor_surface.py                                                  */
# /**************************************************************************/
# /*                         This file is part of:                          */
# /*                                 PYXEL                                  */
# /*                  https://github.com/Ca-Len-Men/Pyxel                   */
# /**************************************************************************/

from pyxel.struct.pcolor import *
from pyxel.struct.pvector import Vector
from pyxel.struct.pixel_creater import *

import numpy
import pygame

keys_border_radius = {'border', 'border_topleft', 'border_topright',
                      'border_bottomleft', 'border_bottomright'}

def scale_grid_pixels(grid_pixels, size):
    source = numpy.array(grid_pixels)
    if source.shape[2] == 4:
        source = source[:, :, :3]

    surface = pygame.surfarray.make_surface(numpy.swapaxes(source, 0, 1))
    return pygame.transform.smoothscale(surface, size)

def new_surface(size, color=NoColor):
    surface = pygame.Surface(size, pygame.SRCALPHA)
    surface.fill(color)
    return surface

flip = pygame.transform.flip

def add_padding(surface, width, color=NoColor):
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

def new_rect(size, color, **kwargs):
    """``Method`` **rect** : drawing rectangle and return the new image.

    - Keys : border, border_topleft, border_topright, border_bottomleft, border_bottomright
    """

    surface = new_surface(size, color)
    pixels = pygame.surfarray.pixels_alpha(surface)
    border_alphas_rect(pixels, **kwargs)
    return surface

def new_rect_width(size, color, width, **kwargs):
    __rect = new_rect(size, color, **kwargs)
    rect_alphas = pygame.surfarray.pixels_alpha(__rect)
    border_alphas_rect(rect_alphas, **kwargs)

    rect_inside = Vector(size[0] - 2 * width, size[1] - 2 * width)
    rect_inside_alphas = numpy.full(rect_inside.tup_int, 255, dtype=numpy.uint8)
    border_alphas_rect(rect_inside_alphas, **kwargs)

    sub_alphas(rect_alphas, rect_inside_alphas, (width, width))
    return __rect

def new_circle(edge: int, color):
    """``Method`` **circle** : drawing circle and return new image."""

    surface = new_surface((edge, edge), color)
    pixels = pygame.surfarray.pixels_alpha(surface)
    border_alphas_rect(pixels, border=edge//2)
    return surface

def new_gaussian_circle(edge: int, color):
    surface = new_surface((edge, edge), color)
    pixels = pygame.surfarray.pixels_alpha(surface)
    gaussian_circle_alpha(pixels, color[3])
    return surface

def fill_mask(surface, color) -> pygame.Surface:
    alphas_of_surface = pygame.surfarray.pixels_alpha(surface)

    fill_surface = new_surface(surface.get_size(), color)
    alphas_of_full_surface = pygame.surfarray.pixels_alpha(fill_surface)
    alphas_of_full_surface[:] = (alphas_of_surface * (color[3] / 255)).round()
    return fill_surface

def insert_to_square(surface, centroid=Vector.zero()):
    """``Method`` **square** : create square image from **surface**,
    with center of square is **centroid** point in **surface**.

    :param surface: image
    :type surface: pygame.Surface
    :param centroid: point in surface
    :return: square image
    """

    size = surface.get_size()
    centroid_vector = Vector(size[0] / 2 + centroid[0], size[1] / 2 + centroid[1])
    x1, x2 = abs(centroid_vector.x), abs(centroid_vector.x - size[0])
    y1, y2 = abs(centroid_vector.y), abs(centroid_vector.y - size[1])
    edge = int(max(x1, x2, y1, y2))

    __new_surface = new_surface((edge * 2, edge * 2))
    __new_surface.blit(surface, Vector(edge, edge) - centroid_vector)
    return __new_surface

def enhancement(surface):
    source = pygame.surfarray.pixels_alpha(surface)
    source[:] = (source * (2 - source / 255)).round()

def linear_gradient_icon(surface, grid_pixels):
    linear_gradient = scale_grid_pixels(grid_pixels, surface.get_size())
    linear_gradient_colors = pygame.surfarray.pixels3d(linear_gradient)
    surface_colors = pygame.surfarray.pixels3d(surface)
    surface_alphas = pygame.surfarray.pixels_alpha(surface)

    predicate = surface_alphas != 0
    surface_colors[predicate] = linear_gradient_colors[predicate]

def border_corner(surface, **kwargs):
    alphas_surf = pygame.surfarray.pixels_alpha(surface)
    border_alphas_rect(alphas_surf, **kwargs)
