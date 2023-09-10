import pygame
from typing import Tuple

class Color(pygame.Color):
    # Basic colors
    NoColor: Color
    Red: Color
    Pink: Color
    Yellow: Color
    Orange: Color
    Green: Color
    Blue: Color
    Purple: Color
    White: Color
    Brown: Color
    Gray: Color
    Black: Color

    # Boostrap colors
    Primary: Color
    Secondary: Color
    Success: Color
    Danger: Color
    Warning: Color
    Info: Color
    Light: Color
    Dark: Color

    # Other colors
    Gold: Color
    LightBlue: Color
    LightCyan: Color
    DarkCyan: Color
    LightGreen: Color
    GreenYellow: Color
    Chocolate: Color
    Violet: Color

    SeaGreen: Color
    DarkSeaGreen: Color
    CadetBlue: Color
    CornflowerBlue: Color
    SlateBlue: Color
    LightSlateBlue: Color
    PeachPuff: Color
    Sienna: Color
    PaleGoldenrod: Color
    DimGray: Color
    Gainsboro: Color
    Silver: Color
    Cyan: Color
    Goldenrod: Color
    LightGoldenrod: Color
    DarkKhaki: Color
    Khaki: Color
    DarkOliveGreen: Color
    ForestGreen: Color
    LawnGreen: Color
    MediumSeaGreen: Color
    SpringGreen: Color
    Maroon: Color
    HotPink: Color
    Rouge: Color
    DarkRed: Color
    Tomato: Color
    OrangeRed: Color
    Firebrick: Color
    Salmon: Color
    IndianRed: Color
    DarkGoldenrod: Color

    def __init__(self, r, g, b, a=255) -> None:...

    def new_alpha(self, alpha) -> Color:...

    @property
    def rgb(self) -> Tuple[int, int, int]:...

    @classmethod
    def random(cls) -> Color:...

    @classmethod
    def init_colors(cls) -> None:...