from typing import *
from weakref import WeakMethod

class Vector(Sequence[float]):
    __x: float
    __y: float

    @classmethod
    def zero(cls) -> Vector:...
    @classmethod
    def left(cls) -> Vector:...
    @classmethod
    def right(cls) -> Vector:...
    @classmethod
    def up(cls) -> Vector:...
    @classmethod
    def down(cls) -> Vector:...
    @classmethod
    def random(cls) -> Vector:...

    @property
    def x(self) -> float:...
    @x.setter
    def x(self, __x: float) -> None:...
    @property
    def y(self) -> float:...
    @y.setter
    def y(self, __y: float) -> None:...
    @property
    def angle(self) -> float:...
    @angle.setter
    def angle(self, __angle: float) -> None:...
    @property
    def tup(self) -> Tuple[float, float]:...
    @tup.setter
    def tup(self, __tup: Tuple[float, float]) -> None:...
    @property
    def tup_int(self) -> Tuple[int, int]:...
    @tup_int.setter
    def tup_int(self, __tup_int: Tuple[int, int]) -> None:...

    def copy(self) -> Vector:...
    def magnitude(self, other: Vector) -> float:...
    def normalize(self) -> Vector:...
    def setxy(self, __x: float, __y: float) -> None:...
    def set(self, source: Union[Tuple[float, float], List[float], Vector]) -> None:...
    def lerp(self, target: Vector, delta: float) -> bool:...

    def __init__(self, x: float, y: float) -> None:...
    def __str__(self) -> str:...
    def __repr__(self) -> str:...
    def __len__(self) -> int:...
    def __iter__(self) -> Generator[float]:...
    def __copy__(self) -> Vector:...

    def __add__(self, other: Vector) -> Vector:...
    def __iadd__(self, other: Vector) -> Vector:...
    def __sub__(self, other: Vector) -> Vector:...
    def __isub__(self, other: Vector) -> Vector:...
    def __mul__(self, other: Union[int, float, Vector]) -> Vector:...
    def __imul__(self, other: Union[int, float, Vector]) -> Vector:...
    def __truediv__(self, val: float) -> Vector:...
    def __itruediv__(self, val: float) -> Vector:...
    def __floordiv__(self, val: int) -> Vector:...
    def __ifloordiv__(self, val: int) -> Vector:...
    def __abs__(self) -> Vector:...
    def __bool__(self) -> bool:...
    def __eq__(self, other: Vector) -> bool:...
    def __ne__(self, other: Vector) -> bool:...
    def __neg__(self) -> Vector:...
    def __float__(self) -> float:...
    def __getitem__(self, i: int) -> float:...
    def __setitem__(self, i: int, _: float) -> None:...

class WeakrefMethod:
    __weakref_bounded_method: WeakMethod
    
    def __init__(self, __bounded_method: Callable[[...], None]) -> None:...
    def __call__(self, *args) -> bool:...

class Delegate:
    _weakref_methods: Optional[Set[WeakrefMethod]]
    
    def __init__(self) -> None:...
    def call(self, *args) -> None:...
    def add(self, __weakref_bounded_method: WeakrefMethod) -> None:...

class VectorListener(Vector):
    __delegate: Delegate

    def __init__(self, __x: float, __y: float) -> None:...
    def add_listener(self, __listener: WeakrefMethod) -> None:...
    def only_set(self, source: Vector) -> None:...
