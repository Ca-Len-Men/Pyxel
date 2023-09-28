# /**************************************************************************/
# /*  asset_model.py                                                        */
# /**************************************************************************/
# /*                         This file is part of:                          */
# /*                                 PYXEL                                  */
# /*                  https://github.com/Ca-Len-Men/Pyxel                   */
# /**************************************************************************/

from pyxel.info import *

import pygame
import pygame.freetype

def load_image(source_path: str):
    result = pygame.image.load(source_path)

    # SRCALPHA not in flags of result
    if not result.get_flags() & pygame.SRCALPHA:
        result = result.convert_alpha()
    return result

class ImageCache:
    """ Lớp ImageCache
    - Trỏ vào một thư mục hình ảnh
    - Cơ chế tải ảnh duy nhất lần đầu tiên.
    - Sau lần tải đầu tiên, ảnh được lưu lại để sử dụng ( gọi là ảnh gốc ),
    nếu thay đổi ảnh gốc, tất cả các phiên bản khác bị thay đổi theo.
    """

    def __init__(self):
        self.__dict_surfaces = {}
        self.__dir = None

    def init(self, dirname: str):
        """ Ánh xạ vào một thư mục. """

        self.__dir = dirname

    def load(self, filename: str):
        """ Chỉ tải ảnh bên trong thư mục được ánh xạ.

        - Chỉ định rõ ràng đuôi mở rộng ( .png, .jpg )
        - Nếu ảnh nằm trong một thư mục con, thêm tên thư mục đó vào.
        - Ví dụ : ``"SubAsset/image.png"``.

        :return: ảnh đã lưu vào **dict** tải
        """

        assert self.__dir is not None, \
            f"From {self.__class__.__name__}.__getitem__ : resource directory not initialized !"

        key_path = f'{self.__dir}/{filename}'
        result = self.__dict_surfaces.get(key_path)

        if result is None:
            result = load_image(key_path)
            self.__dict_surfaces[filename] = result
        return result

class ImageDownloader:
    """ Lớp ImageDownloader
    - Trỏ vào một thư mục hình ảnh
    - Tải ảnh từ tệp hình ảnh nhiều lần.
    - Mỗi phiên bản hình ảnh sau khi "load" là khác nhau.
    """

    def __init__(self, dirname: str):
        self.__dir = dirname

    def load(self, filename: str):
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
