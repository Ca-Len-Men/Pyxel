#cython: language_level=3

import pygame
import random

class Color(pygame.Color):
    # Basic colors
    NoColor: 'Color' = None
    Red: 'Color' = None
    Pink: 'Color' = None
    Yellow: 'Color' = None
    Orange: 'Color' = None
    Green: 'Color' = None
    Blue: 'Color' = None
    Purple: 'Color' = None
    White: 'Color' = None
    Brown: 'Color' = None
    Gray: 'Color' = None
    Black: 'Color' = None

    # Boostrap colors
    Primary: 'Color' = None
    Secondary: 'Color' = None
    Success: 'Color' = None
    Danger: 'Color' = None
    Warning: 'Color' = None
    Info: 'Color' = None
    Light: 'Color' = None
    Dark: 'Color' = None

    # Other colors
    Gold: 'Color' = None
    LightBlue: 'Color' = None
    LightCyan: 'Color' = None
    DarkCyan: 'Color' = None
    LightGreen: 'Color' = None
    GreenYellow: 'Color' = None
    Chocolate: 'Color' = None
    Violet: 'Color' = None

    SeaGreen: 'Color' = None
    DarkSeaGreen: 'Color' = None
    CadetBlue: 'Color' = None
    CornflowerBlue: 'Color' = None
    SlateBlue: 'Color' = None
    LightSlateBlue: 'Color' = None
    PeachPuff: 'Color' = None
    Sienna: 'Color' = None
    PaleGoldenrod: 'Color' = None
    DimGray: 'Color' = None
    Gainsboro: 'Color' = None
    Silver: 'Color' = None
    Cyan: 'Color' = None
    Goldenrod: 'Color' = None
    LightGoldenrod: 'Color' = None
    DarkKhaki: 'Color' = None
    Khaki: 'Color' = None
    DarkOliveGreen: 'Color' = None
    ForestGreen: 'Color' = None
    LawnGreen: 'Color' = None
    MediumSeaGreen: 'Color' = None
    SpringGreen: 'Color' = None
    Maroon: 'Color' = None
    HotPink: 'Color' = None
    Rouge: 'Color' = None
    DarkRed: 'Color' = None
    Tomato: 'Color' = None
    OrangeRed: 'Color' = None
    Firebrick: 'Color' = None
    Salmon: 'Color' = None
    IndianRed: 'Color' = None
    DarkGoldenrod: 'Color' = None

    def __init__(self, r, g, b, a=255):
        super().__init__(r, g, b, a)

    def new_alpha(self, alpha):
        return self.__class__(self.r, self.g, self.b, alpha)

    @property
    def rgb(self):
        return tuple(self[:3])

    @classmethod
    def random(cls):
        return cls(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 255)

    @classmethod
    def init_colors(cls):
        # Basic colors
        Color.NoColor = cls(0, 0, 0, 0)
        Color.Red = cls(255, 0, 0, 255)
        Color.Pink = cls(255, 192, 203, 255)
        Color.Yellow = cls(255, 255, 0, 255)
        Color.Orange = cls(255, 165, 0, 255)
        Color.Green = cls(0, 255, 0, 255)
        Color.Blue = cls(0, 0, 255, 255)
        Color.Purple = cls(128, 0, 128, 255)
        Color.White = cls(255, 255, 255, 255)
        Color.Brown = cls(165, 42, 42, 255)
        Color.Gray = cls(128, 128, 128, 255)
        Color.Black = cls(0, 0, 0, 255)

        # Bootstrap colors
        Color.Primary = cls(13, 110, 253, 255)
        Color.Secondary = cls(108, 117, 125, 255)
        Color.Success = cls(25, 135, 84, 255)
        Color.Danger = cls(220, 53, 69, 255)
        Color.Warning = cls(255, 193, 7, 255)
        Color.Info = cls(23, 162, 184, 255)
        Color.Light = cls(248, 249, 250, 255)
        Color.Dark = cls(52, 58, 64, 255)

        # Other colors
        Color.Gold = cls(255, 215, 0, 255)
        Color.LightBlue = cls(173, 216, 230, 255)
        Color.LightCyan = cls(224, 255, 255, 255)
        Color.DarkCyan = cls(0, 139, 139, 255)
        Color.LightGreen = cls(144, 238, 144, 255)
        Color.GreenYellow = cls(173, 255, 47, 255)
        Color.Chocolate = cls(210, 105, 30, 255)
        Color.Violet = cls(238, 130, 238, 255)

        Color.Cyan = cls(0, 255, 255, 255)
        Color.Silver = cls(192, 192, 192, 255)
        Color.Gainsboro = cls(220, 220, 220, 255)
        Color.DimGray = cls(105, 105, 105, 255)
        Color.PaleGoldenrod = cls(238, 232, 170, 255)
        Color.Sienna = cls(160, 82, 45, 255)
        Color.PeachPuff = cls(255, 218, 185, 255)
        Color.LightSlateBlue = cls(132, 112, 255, 255)
        Color.SlateBlue = cls(106, 90, 205, 255)
        Color.CornflowerBlue = cls(100, 149, 237, 255)
        Color.CadetBlue = cls(95, 158, 160, 255)
        Color.DarkSeaGreen = cls(143, 188, 143, 255)
        Color.SeaGreen = cls(46, 139, 87, 255)
        Color.SpringGreen = cls(0, 255, 127, 255)
        Color.MediumSeaGreen = cls(60, 179, 113, 255)
        Color.LawnGreen = cls(124, 252, 0, 255)
        Color.ForestGreen = cls(34, 139, 34, 255)
        Color.DarkOliveGreen = cls(85, 107, 47, 255)
        Color.Khaki = cls(255, 246, 143, 255)
        Color.DarkKhaki = cls(189, 183, 107, 255)
        Color.LightGoldenrod = cls(238, 221, 130, 255)
        Color.Goldenrod = cls(218, 165, 32, 255)
        Color.DarkGoldenrod = cls(184, 134, 11, 255)
        Color.IndianRed = cls(205, 92, 92, 255)
        Color.Firebrick = cls(178, 34, 34, 255)
        Color.Salmon = cls(250, 128, 114, 255)
        Color.OrangeRed = cls(255, 69, 0, 255)
        Color.Tomato = cls(255, 99, 71, 255)
        Color.DarkRed = cls(139, 0, 0, 255)
        Color.Rouge = cls(198, 0, 0, 255)
        Color.HotPink = cls(255, 105, 180, 255)
        Color.Maroon = cls(176, 48, 96, 255)

Color.init_colors()