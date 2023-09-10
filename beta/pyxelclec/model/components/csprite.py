from pyxelclec.__info__ import package_name
from pyxelclec.__flag__ import FLAG_NO_RENDER
from pyxelclec.asset import image_cache, font_cache, FontCache
from pyxelclec.geo.draw import sub_alphas
from pyxelclec.geo.frect import Rect, StructRect
from pyxelclec.geo.fvector import Vector, WeakrefMethod
from pyxelclec.geo.color import Color
from pyxelclec.model.component import Component, MANY
from .cscript import ComponentScript
from .ccollider import ComponentCollider

from abc import abstractmethod
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

class ComponentSprite(Component, Rect):
    def __init__(self, surface=None):
        Component.__init__(self)
        self._dist = Vector.zero()
        self._area = None  # Collider of entity
        self._mask = None       # Mask ( 2-d array alpha bit ) of Surface

        if surface is None:
            Rect.__init__(self, Vector.zero())
            self._CONSTANT_SURFACE = self._SURFACE = None
        else:
            self._CONSTANT_SURFACE = surface
            if isinstance(surface, str):
                surface = image_cache.load(surface)

            self._SURFACE = surface
            Rect.__init__(self, Vector(*surface.get_size()))
            self.size_listener(WeakrefMethod(self.__resize_listener))

    def __resize_listener(self, size):
        if self.surface.get_size() != self.size.tup_int:
            self.resize(size.tup_int)

    def __moving_listener(self, topleft):
        self._dist = topleft - self._area.topleft

    def __area_moving_listener(self, topleft):
        self.only_set_topleft(topleft + self._dist)

    def research(self, entity):
        self._area = entity.collider
        assert self._area, f"From {self.__class__.__name__}.research : " \
                                f"entity must have ComponentCollider's instance !"

        # If the position of this sprite is changed, recalculate the '_dist' vector.
        self.pos_listener(WeakrefMethod(self.__moving_listener))

        # If the position of this collider is changed, recalculate the '_position' vector.
        self._area.pos_listener(WeakrefMethod(self.__area_moving_listener))

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

    @surface.setter
    def surface(self, __surface):
        self._CONSTANT_SURFACE = self._SURFACE = __surface
        self.size = Vector(*__surface.get_size())
        self._mask = None

    @property
    def surfconst(self):
        assert self._CONSTANT_SURFACE, f"From {self.__class__.__name__}.surface : " \
                                       f"sprite at {id(self)} is invalid !"

        # When user call it, by default, it don't change, and shouldn't change it.
        return self._SURFACE

    @property
    def mask(self):
        if self._mask is None:
            self._mask = pygame.mask.from_surface(self._SURFACE)
        return self._mask

    @mask.deleter
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
        bg_rect = StructRect(self.size)

        if isinstance(icon, pygame.Surface):
            icon_alphas = pygame.surfarray.pixels_alpha(icon)
            icon_rect = StructRect(*icon.get_size())
        elif isinstance(icon, CSprite):
            icon_alphas = pygame.surfarray.pixels_alpha(icon.surfconst)
            icon_rect = StructRect(Vector(*icon.size))
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
            self.entity.canvas.sprite.blit_sprite(self)

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
                rect = StructRect(Vector(*sprite.get_size()))
                self_rect = StructRect(self.size)
                setattr(rect, dest, getattr(self_rect, dest))
                self.surface.blit(sprite, rect.topleft)
            case 0b010_001_010:  # dest: Vector & BLIT_MASK
                source_alphas_copy = pygame.surfarray.pixels_alpha(self.surface).copy()
                self.surface.blit(sprite, dest)
                source_alphas = pygame.surfarray.pixels_alpha(self.surface)
                source_alphas[:] = source_alphas_copy
            case 0b011_001_010:  # dest: str & BLIT_MASK
                source_alphas_copy = pygame.surfarray.pixels_alpha(self.surface).copy()
                rect = StructRect(Vector(*sprite.get_size()))
                self_rect = StructRect(self.size)
                setattr(rect, dest, getattr(self_rect, dest))
                self.surface.blit(sprite, rect.topleft)
                source_alphas = pygame.surfarray.pixels_alpha(self.surface)
                source_alphas[:] = source_alphas_copy

            # sprite: CSprite
            case 0b001_010_001:  # dest = None & BLIT_NORMAL
                self.surface.blit(sprite.surfconst, sprite.topleft)
            case 0b001_010_010:  # dest = None & BLIT_MASK
                source_alphas_copy = pygame.surfarray.pixels_alpha(self.surface).copy()
                self.surface.blit(sprite.surfconst, sprite.topleft)
                source_alphas = pygame.surfarray.pixels_alpha(self.surface)
                source_alphas[:] = source_alphas_copy
            case _:
                print(f'From {self.__class__.__name__}.blit : do nothing !')

    def resize(self, size_type):
        # Parameter type of 'size_type' must be <int, float, Vector, Tuple[int, int]>.
        #   + For type <int, float, Vector> : resize with percent.
        #   + For type <Tuple[int, int]>     : resize equal size (int, int).

        if isinstance(size_type, (int, float, Vector)):
            new_size = self.size * size_type
            if self.surface.get_size() == new_size.tup_int:
                return
            self.only_set_size(new_size)
        elif isinstance(size_type, tuple) and \
                isinstance(size_type[0], int) and isinstance(size_type[1], int):
            # Fixed size
            if self.surface.get_size() == self.size.tup_int:
                return
            self.only_set_size(Vector(*size_type))
        else:
            raise TypeError(f'From {self.__class__.__name__}.resize : '
                            f'type of parameter `float_tuple2_Vector` '
                            f'must be <int, float, Vector, Tuple[int, int]> !')

        surface_to_scale = self._CONSTANT_SURFACE
        if isinstance(self._CONSTANT_SURFACE, str):
            surface_to_scale = image_cache.load(self._CONSTANT_SURFACE)
        self._SURFACE = pygame.transform.smoothscale(surface_to_scale, abs(self.size).tup_int)

        flip_x, flip_y = self.size.x < 0, self.size.y < 0
        if flip_x or flip_y:
            source_array = pygame.surfarray.pixels3d(self._SURFACE)
            source_array[:] = source_array[slice(None, None, -1) if flip_x else slice(None),
            slice(None, None, -1) if flip_y else slice(None)]

    @abstractmethod
    def copy(self): pass

    def copy_source(self, source):
        assert self.size.tup_int == source.size.tup_int, \
            f"from {self.__class__.__name__}.copy_source : two sprite must be same size !"

        __self_pixels = pygame.surfarray.pixels3d(self.surface)
        __self_alphas = pygame.surfarray.pixels_alpha(self.surface)
        __self_pixels[:] = pygame.surfarray.pixels3d(source.surface)
        __self_alphas[:] = pygame.surfarray.pixels_alpha(source.surface)

    def __copy__(self):
        return self.copy()

    @classmethod
    def quantity(cls):
        return MANY

    @classmethod
    def get_comp(cls):
        return ComponentSprite

class CSprite(ComponentSprite):
    def copy(self):
        return CSprite(self._SURFACE.copy())

class CMask(ComponentCollider):
    def __init__(self):
        super().__init__(0, 0)
        self._mask = None
        self._sprite = None

    def __resize_listener(self, size):
        self.only_set_size(size)

    def research(self, entity):
        self._sprite = entity.get_component(ComponentSprite)
        self.size = self._sprite.size
        self._sprite.size_listener(WeakrefMethod(self.__resize_listener))

    def collide_point(self, point: Vector):
        if super().collide_point(point):
            topleft = point - self.topleft

            if self._mask is None:
                self._mask = pygame.mask.from_surface(self._sprite.surfconst)
            return self._mask.get_at(topleft)
        return False

class CLabel(CSprite):
    keys = {'text', 'color', 'font_size', 'style', 'font_name', 'enhance_opacity'}

    def __init__(self, **kwargs):
        self._text = package_name
        self._font_size = 18
        self._color = Color.White
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
        """ Keys :
        + Type of label : text, color, font_size, style, font_name.
        + Position : topleft, bottomleft, ... .
        """

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
