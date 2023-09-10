from pyxelclec.__info__ import *

import pygame
import pygame.freetype

def load_image(source_path):
    result = pygame.image.load(source_path)

    # SRCALPHA not in flags of result
    if not result.get_flags() & pygame.SRCALPHA:
        result = result.convert_alpha()
    return result

class ImageCache:
    def __init__(self):
        self.__dict_pictures = {}
        self.__dir = None

    def init(self, dirname):
        self.__dir = dirname

    def load(self, filename):
        assert self.__dir is not None, \
            f"From {self.__class__.__name__}.__getitem__ : resource directory not initialized !"

        key_path = f'{self.__dir}/{filename}'
        result = self.__dict_pictures.get(key_path)

        if result is None:
            result = load_image(key_path)
            self.__dict_pictures[filename] = result
        return result

class ImageDownloader:
    def __init__(self, dirname):
        self.__dir = dirname

    def load(self, filename):
        path = f'{self.__dir}/{filename}'
        return load_image(path)

class FontCache:
    default = 'Texturina-Medium'

    def __init__(self):
        self.__dict_fonts = {}
        self.__dir = f'{package_path}\\fonts'

    def load(self, filename):
        key_path = f'{self.__dir}\\{filename}.ttf'
        result = self.__dict_fonts.get(key_path)

        if result is None:
            result = pygame.freetype.Font(key_path)
            self.__dict_fonts[filename] = result
        return result

image_cache = ImageCache()
image_cache.init(f'{package_path}/icons')
font_cache = FontCache()
# image_downloader = ImageDownloader(f'{package_path}/icons')

if __name__ == '__main__':
    pass
