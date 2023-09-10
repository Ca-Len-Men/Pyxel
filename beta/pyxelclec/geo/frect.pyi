from .fvector import *

class StructRect:
    _position: Vector
    _size: Vector
    size: Vector
    w: float
    h: float
    center: Vector
    topleft: Vector
    topright: Vector
    bottomleft: Vector
    bottomright: Vector
    midtop: Vector
    midbottom: Vector
    midleft: Vector
    midright: Vector
    midx: float
    midy: float

    def __init__(self, size: Vector, position=None) -> None:...
    def collide_point(self, point: Vector) -> bool:...


class Rect(StructRect):
    _size: VectorListener
    _position: VectorListener

    def __init__(self, size: Vector, position=None) -> None:...
    def size_listener(self, __listener: WeakrefMethod) -> None:...
    def pos_listener(self, __listener: WeakrefMethod) -> None:...
    def only_set_size(self, __size: Vector) -> None:...
    def only_set_topleft(self, __topleft: Vector) -> None:...
