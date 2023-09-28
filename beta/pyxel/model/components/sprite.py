# /**************************************************************************/
# /*  sprite.py                                                             */
# /**************************************************************************/
# /*                         This file is part of:                          */
# /*                                 PYXEL                                  */
# /*                  https://github.com/Ca-Len-Men/Pyxel                   */
# /**************************************************************************/

from pyxel.system_warning import warning_report
from pyxel.info import package_name, FLAG_NO_RENDER
from pyxel.asset_model import image_cache, font_cache, FontCache
from pyxel.struct.pixel_creater import sub_alphas
from pyxel.struct.prect import Rect
from pyxel.struct.pvector import Vector, VectorDependent
from pyxel.struct.pcolor import *
from pyxel.model.component import Component
from pyxel.model.components.script import ComponentScript
from pyxel.model.components.collider import ComponentCollider

import pygame.freetype
import numpy

BLIT_NORMAL = 0b001
BLIT_MASK = 0b010

STYLE_DEFAULT = pygame.freetype.STYLE_DEFAULT
STYLE_UNDERLINE = pygame.freetype.STYLE_UNDERLINE
STYLE_OBLIQUE = pygame.freetype.STYLE_OBLIQUE
STYLE_NORMAL = pygame.freetype.STYLE_NORMAL
STYLE_STRONG = pygame.freetype.STYLE_STRONG
STYLE_WIDE = pygame.freetype.STYLE_WIDE

# Surface in Sprite :
#   + CONSTANT SURFACE : you shouldn't change it.
#   + Surface          : you can change, blit on, resize it.
# ----------
# - Behaviour :
#   + (1) For resize : the CONSTANT SURFACE is used to resize to Surface.
#   + (2) For other changing : changed the Surface and the CONSTANT SURFACE is replaced by Surface.
#   + (3) When we get the `surface` property : by default, the surface will be change and go back to step (2).
#   + (4) If the Surface have been change : deleted the mask of Surface, so shouldn't reference the mask.

# Specially, the `resource` is used to mapping the string path to the image file ( Surface )
# and cached it, so the CONSTANT_SURFACE can be the `str` type.

class ComponentSprite(Component):
    def __init__(self, surface=None):
        warning_report.add(self)
        Component.__init__(self)
        self._mask = None  # Mask ( 2-d array alpha bit ) of Surface
        self.__rect = Rect(Vector(0, 0), position=VectorDependent(0, 0))
        self.rect.get_size().delegate.add(self, ComponentSprite._event_size_changed)

        if surface is None:
            self._CONSTANT_SURFACE = self._SURFACE = None
        else:
            self._CONSTANT_SURFACE = surface
            if isinstance(surface, str):
                surface = image_cache.load(surface)

            self._SURFACE = surface
            self.rect.get_size().only_set(surface.get_size())

    def warning(self):
        if self._CONSTANT_SURFACE is None:
            print(f'Warning: CSprite at {id(self)} chưa khởi tạo Surface !')

    def _event_size_changed(self, size: Vector):
        """ Thay đổi kích thước ảnh bằng đúng với **size**. """

        # Kích thước không thay đổi
        if self.surface.get_size() == size.tup_int:
            return

        surface_to_scale = self._CONSTANT_SURFACE
        if isinstance(self._CONSTANT_SURFACE, str):
            surface_to_scale = image_cache.load(self._CONSTANT_SURFACE)
        self._SURFACE = pygame.transform.smoothscale(surface_to_scale, abs(size).tup_int)

        flip_x, flip_y = self.rect.w < 0, self.rect.h < 0
        if flip_x or flip_y:
            # Đảo chiều Surface
            source_array = pygame.surfarray.pixels3d(self._SURFACE)
            source_array[:] = source_array[slice(None, None, -1) if flip_x else slice(None),
            slice(None, None, -1) if flip_y else slice(None)]

        # Kích thước không được phép âm
        self.rect.get_size().only_set(abs(size))

    def research(self, entity):
        # Phụ thuộc tương đối vào vị trí của entity
        self.rect.get_position().set_ref(entity.rect.get_position())  # type: ignore

    @property
    def rect(self):
        return self.__rect

    @property
    def surface(self):
        # By default, the Surface will be change, so we do ( :
        # + If CONSTANT SURFACE is `str` type : we can copy it from `resource`.
        # + Otherwise                         : replace the CONSTANT SURFACE by the Surface.

        assert self._CONSTANT_SURFACE, f"From {self.__class__.__name__}.surface : " \
                                       f"sprite at {id(self)} is invalid !"

        if isinstance(self._CONSTANT_SURFACE, str):
            self._SURFACE = self._SURFACE.copy()
        self._CONSTANT_SURFACE = self._SURFACE
        self._mask = None
        return self._SURFACE

    @surface.setter  # type: ignore
    def surface(self, __surface: pygame.Surface):
        self._CONSTANT_SURFACE = self._SURFACE = __surface
        self.rect.size = __surface.get_size()
        self._mask = None

    @property
    def surfconst(self):
        assert self._CONSTANT_SURFACE, f"From {self.__class__.__name__}.surface : " \
                                       f"sprite at {id(self)} is invalid !"

        # When user call it, by default, it don't change, and shouldn't change it.
        return self._SURFACE

    @property
    def has_surface(self):
        return self._CONSTANT_SURFACE is not None

    @property
    def mask(self):
        if self._mask is None:
            self._mask = pygame.mask.from_surface(self._SURFACE)
        return self._mask

    @mask.deleter  # type: ignore
    def mask(self):
        self._mask = None

    def reorder_depth(self, depth):
        mapping_ = {'r': 0, 'g': 1, 'b': 2}
        source_array = pygame.surfarray.pixels3d(self.surface)
        source_array[:] = source_array[:, :, (mapping_[c] for c in depth)]

    def sub(self, icon, position_type):
        # Parameter type of `position_type` must be <str, Tuple[str, Vector]>
        # Example :
        #       + (1) : sub(..., 'center') or sub(..., 'bottomleft')
        #       + (2) : sub(..., ('center', Vector(...))
        #       meaning we put the 'center' of 'icon' at this 'Vector' position.

        bg_alphas = pygame.surfarray.pixels_alpha(self.surface)
        bg_rect = Rect(self.rect.size)

        if isinstance(icon, pygame.Surface):
            icon_alphas = pygame.surfarray.pixels_alpha(icon)
            icon_rect = Rect(*icon.get_size())
        elif isinstance(icon, CSprite):
            icon_alphas = pygame.surfarray.pixels_alpha(icon.surfconst)
            icon_rect = Rect(Vector(*icon.rect.size))
        else:
            raise TypeError(f'From {self.__class__.__name__}.sub : '
                            f'parameter type of `icon` must be <pygame.Surface, CSprite> !')

        if isinstance(position_type, str):
            setattr(icon_rect, position_type, getattr(bg_rect, position_type))
        elif isinstance(position_type, tuple):
            setattr(icon_rect, position_type[0], position_type[1])
        else:
            raise TypeError(f'From {self.__class__.__name__}.sub : '
                            f'parameter type of `position_type` must be <str, Tuple[str, Vector]> !')

        sub_alphas(bg_alphas, icon_alphas, icon_rect.topleft.tup_int)

    def fill(self, rgb=None, alpha=None):
        if rgb is None and alpha is None:
            return

        source_alphas = pygame.surfarray.pixels_alpha(self.surface)
        condition = source_alphas != 0

        if rgb:
            source_pixels = pygame.surfarray.pixels3d(self.surface)
            source_pixels[condition] = rgb
        if alpha is not None:

            if alpha == 0:
                source_alphas[condition] = alpha
            else:
                __max = numpy.max(source_alphas)
                source_alphas[condition] = source_alphas[condition] * (alpha / __max)

    def enhance_opacity(self, num=1):
        source = pygame.surfarray.pixels_alpha(self.surface)
        for _ in range(num):
            source[:] = (source * (2 - source / 255)).round()

    def update(self):
        if self.entity.virtual_visible:
            # Gọi CCanvas.blit_sprite
            self.entity.canvas.sprite.blit_sprite(self)  # type: ignore

    def blit(self, sprite, dest=None, flag=BLIT_NORMAL):
        # We have many subcase :
        #   + 'dest' : None | Vector or Tuple | str
        #   + 'sprite' : pygame.Surface | CSprite
        #   + 'flag' : BLIT_NORMAL | BLIT_MASK

        if dest is None:
            dest_flag = 0b001_000_000
        elif isinstance(dest, (Vector, tuple)):
            dest_flag = 0b010_000_000
        elif isinstance(dest, str):
            dest_flag = 0b011_000_000
        else:
            raise TypeError(f'From {self.__class__.__name__}.blit : '
                            f'parameter type of `sprite` must be <str, tuple, Vector> !')

        if isinstance(sprite, pygame.Surface):
            sprite_flag = 0b000_001_000
        elif isinstance(sprite, CSprite):
            sprite_flag = 0b000_010_000
        else:
            raise TypeError(f'From {self.__class__.__name__}.blit : '
                            f'parameter type of `sprite` must be <pygame.Surface, CSprite> !')

        match dest_flag | flag | sprite_flag:
            # sprite: Surface
            case 0b010_001_001:  # dest: Vector & BLIT_NORMAL
                self.surface.blit(sprite, dest)
            case 0b011_001_001:  # dest: str & BLIT_NORMAL
                rect = Rect(Vector(*sprite.get_size()))
                self_rect = Rect(self.rect.size)
                setattr(rect, dest, getattr(self_rect, dest))
                self.surface.blit(sprite, rect.topleft)
            case 0b010_001_010:  # dest: Vector & BLIT_MASK
                source_alphas_copy = pygame.surfarray.pixels_alpha(self.surface).copy()
                self.surface.blit(sprite, dest)
                source_alphas = pygame.surfarray.pixels_alpha(self.surface)
                source_alphas[:] = source_alphas_copy
            case 0b011_001_010:  # dest: str & BLIT_MASK
                source_alphas_copy = pygame.surfarray.pixels_alpha(self.surface).copy()
                rect = Rect(Vector(*sprite.get_size()))
                self_rect = Rect(self.rect.size)
                setattr(rect, dest, getattr(self_rect, dest))
                self.surface.blit(sprite, rect.topleft)
                source_alphas = pygame.surfarray.pixels_alpha(self.surface)
                source_alphas[:] = source_alphas_copy

            # sprite: CSprite
            case 0b001_010_001:  # dest = None & BLIT_NORMAL
                self.surface.blit(sprite.surfconst, sprite.rect.topleft)
            case 0b001_010_010:  # dest = None & BLIT_MASK
                source_alphas_copy = pygame.surfarray.pixels_alpha(self.surface).copy()
                self.surface.blit(sprite.surfconst, sprite.rect.topleft)
                source_alphas = pygame.surfarray.pixels_alpha(self.surface)
                source_alphas[:] = source_alphas_copy
            case _:
                print(f'From {self.__class__.__name__}.blit : do nothing !')

    def resize(self, size_type):
        """ Thay đổi kích thước hình ảnh.

        - Nếu **size_type** là ``int``, ``float``, ``Vector`` : kích thước cũ nhân thêm **size_type**.
        - Nếu **size_type** là ``Tuple[int, int]`` : kích thước mới là **size_type**.

        :param size_type: kích thước mới hoặc chỉ định phần trăm kích thước mới
        """

        if isinstance(size_type, (int, float, Vector)):
            self.rect.size *= size_type
        elif isinstance(size_type, tuple) and \
                isinstance(size_type[0], int) and isinstance(size_type[1], int):
            self.rect.size = size_type
        else:
            raise TypeError(f'From {self.__class__.__name__}.resize : '
                            f'type of parameter `float_tuple2_Vector` '
                            f'must be <int, float, Vector, Tuple[int, int]> !')

    def copy(self):
        return ComponentSprite(self.surfconst.copy())

    def copy_from_source(self, source):
        assert self.rect.size.tup_int == source.rect.size.tup_int, \
            f"from {self.__class__.__name__}.copy_source : two sprite must be same size !"

        __self_pixels = pygame.surfarray.pixels3d(self.surface)
        __self_alphas = pygame.surfarray.pixels_alpha(self.surface)
        __self_pixels[:] = pygame.surfarray.pixels3d(source.surface)
        __self_alphas[:] = pygame.surfarray.pixels_alpha(source.surface)

    def __copy__(self):
        return self.copy()

    def __hash__(self):
        return id(ComponentSprite)

class CSprite(ComponentSprite):
    def copy(self):
        return CSprite(self.surfconst.copy())

class CMask(ComponentCollider):
    def __init__(self):
        super().__init__(Vector(0, 0))
        self._sprite = None

    @property
    def sprite(self):
        return self._sprite

    @sprite.setter
    def sprite(self, __sprite: CSprite):
        self._sprite = __sprite
        self.rect.get_position().only_set(__sprite.rect.topleft)
        self.rect.get_size().only_set(__sprite.rect.size)

        __sprite.rect.get_position().delegate.add(self, CMask._event_size_or_position_changed)
        __sprite.rect.get_size().delegate.add(self, CMask._event_size_or_position_changed)

    def _event_size_or_position_changed(self, __vector: Vector):
        """ ``self.rect`` cần phải khớp với ``self._sprite.rect``.
        :param __vector: là ``size`` hoặc ``position`` của ``self._sprite.rect``
        """

        # Kiểm tra `__vector` là `size` hay `position` ?
        if self._sprite.rect.get_position() is __vector:
            self.rect.get_position().only_set(__vector)
        else:
            self.rect.get_size().only_set(__vector)

    def collide_point(self, point: Vector):
        if self.rect.collide_point(point):
            topleft = point - self.rect.topleft
            return self._sprite.mask.get_at(topleft)
        return False

class CLabel(CSprite):
    # Các thuộc tính của CLabel, dùng làm khóa cho phương thức `CLabel.set`
    keys = {'text', 'color', 'font_size', 'style', 'font_name', 'enhance_opacity'}

    def __init__(self, **kwargs):
        self._text = package_name
        self._font_size = 18
        self._color = White
        self._style = STYLE_DEFAULT
        self._font_name = FontCache.default
        self._enhance_opacity = 0

        super().__init__()
        self.set(**kwargs)

    def _render_source(self):
        self.surface = font_cache.load(self._font_name).render(
            text=self._text,
            fgcolor=self._color,
            style=self._style,
            size=self._font_size
        )[0]
        self.enhance_opacity(self._enhance_opacity)

    def set(self, **kwargs):
        if not kwargs:
            self._render_source()
            return

        __keys = CLabel.keys.intersection(kwargs)
        for key in __keys:
            setattr(self, f'_{key}', kwargs[key])

        if FLAG_NO_RENDER not in kwargs:
            self._render_source()
        return self

    @property
    def text(self):
        return self._text

    @text.setter  # type: ignore
    def text(self, __text):
        if self._text != __text:
            self._text = __text
            self._render_source()

    @property
    def color(self):
        return self._color

    @color.setter  # type: ignore
    def color(self, __color):
        if self._color != __color:
            self._color = __color
            self._render_source()

    @property
    def font_size(self):
        return self._font_size

    @font_size.setter  # type: ignore
    def font_size(self, __font_size):
        if self._font_size != __font_size:
            self._font_size = __font_size
            self._render_source()

    @property
    def style(self):
        return self._style

    @style.setter  # type: ignore
    def style(self, __style):
        if self._style != __style:
            self._style = __style
            self._render_source()

    @property
    def font_name(self):
        return self._font_name

    @font_name.setter  # type: ignore
    def font_name(self, __font_name):
        if self._font_name != __font_name:
            self._font_name = __font_name
            self._render_source()

class ScriptShowAllCSprite(ComponentScript):
    def update(self):
        for sprite in self.entity.get_component(ComponentSprite, get_all=True):
            sprite.update()
