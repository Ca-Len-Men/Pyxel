# /**************************************************************************/
# /*  ppy                                                             */
# /**************************************************************************/
# /*                         This file is part of:                          */
# /*                                 PYXEL                                  */
# /*                  https://github.com/Ca-Len-Men/Pyxel                   */
# /**************************************************************************/

import pygame
import random

class Color(pygame.Color):
    def __init__(self, r, g, b, a=255):
        super().__init__(r, g, b, a)

    def new_alpha(self, __alpha: int):
        return self.__class__(self.r, self.g, self.b, __alpha)

    @property
    def rgb(self):
        return tuple(self[:3])

    @classmethod
    def random(cls):
        return cls(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    
# Basic colors
NoColor = Color(0, 0, 0, 0)
Red = Color(255, 0, 0, 255)
Pink = Color(255, 192, 203, 255)
Yellow = Color(255, 255, 0, 255)
Orange = Color(255, 165, 0, 255)
Green = Color(0, 255, 0, 255)
Blue = Color(0, 0, 255, 255)
Purple = Color(128, 0, 128, 255)
White = Color(255, 255, 255, 255)
Brown = Color(165, 42, 42, 255)
Gray = Color(128, 128, 128, 255)
Black = Color(0, 0, 0, 255)

# Bootstrap colors
Primary = Color(13, 110, 253, 255)
Secondary = Color(108, 117, 125, 255)
Success = Color(25, 135, 84, 255)
Danger = Color(220, 53, 69, 255)
Warning = Color(255, 193, 7, 255)
Info = Color(23, 162, 184, 255)
Light = Color(248, 249, 250, 255)
Dark = Color(52, 58, 64, 255)

# Other colors
Gold = Color(255, 215, 0, 255)
LightBlue = Color(173, 216, 230, 255)
LightCyan = Color(224, 255, 255, 255)
DarkCyan = Color(0, 139, 139, 255)
LightGreen = Color(144, 238, 144, 255)
GreenYellow = Color(173, 255, 47, 255)
Chocolate = Color(210, 105, 30, 255)
Violet = Color(238, 130, 238, 255)

Cyan = Color(0, 255, 255, 255)
Silver = Color(192, 192, 192, 255)
Gainsboro = Color(220, 220, 220, 255)
DimGray = Color(105, 105, 105, 255)
PaleGoldenrod = Color(238, 232, 170, 255)
Sienna = Color(160, 82, 45, 255)
PeachPuff = Color(255, 218, 185, 255)
LightSlateBlue = Color(132, 112, 255, 255)
SlateBlue = Color(106, 90, 205, 255)
CornflowerBlue = Color(100, 149, 237, 255)
CadetBlue = Color(95, 158, 160, 255)
DarkSeaGreen = Color(143, 188, 143, 255)
SeaGreen = Color(46, 139, 87, 255)
SpringGreen = Color(0, 255, 127, 255)
MediumSeaGreen = Color(60, 179, 113, 255)
LawnGreen = Color(124, 252, 0, 255)
ForestGreen = Color(34, 139, 34, 255)
DarkOliveGreen = Color(85, 107, 47, 255)
Khaki = Color(255, 246, 143, 255)
DarkKhaki = Color(189, 183, 107, 255)
LightGoldenrod = Color(238, 221, 130, 255)
Goldenrod = Color(218, 165, 32, 255)
DarkGoldenrod = Color(184, 134, 11, 255)
IndianRed = Color(205, 92, 92, 255)
Firebrick = Color(178, 34, 34, 255)
Salmon = Color(250, 128, 114, 255)
OrangeRed = Color(255, 69, 0, 255)
Tomato = Color(255, 99, 71, 255)
DarkRed = Color(139, 0, 0, 255)
Rouge = Color(198, 0, 0, 255)
HotPink = Color(255, 105, 180, 255)
Maroon = Color(176, 48, 96, 255)
