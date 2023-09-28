# /**************************************************************************/
# /*  base.py                                                               */
# /**************************************************************************/
# /*                         This file is part of:                          */
# /*                                 PYXEL                                  */
# /*                  https://github.com/Ca-Len-Men/Pyxel                   */
# /**************************************************************************/

from pyxel.model.canvas import root, update_behaviour

import sys
import pygame
import pygame.freetype

class TimeInput:
    def __init__(self):
        self.__clock = pygame.time.Clock()
        self.__fps = 0
        self.delta_time: float = 0
        self.delta_time_milliseconds = 0

    @property
    def fps(self):
        return self.__clock.get_fps()

    @fps.setter     # type: ignore
    def fps(self, _: int):
        self.__fps = _

    def update(self):
        self.delta_time_milliseconds = self.__clock.tick(self.__fps)
        self.delta_time = self.delta_time_milliseconds / 1000

class GameSystem:
    def init(self, size, caption=None, icon_path=None):
        pygame.display.set_mode(size)
        root.init()

        if caption:
            pygame.display.set_caption(caption)
        if icon_path:
            pygame.display.set_icon(pygame.image.load(icon_path))

    def __init__(self):
        super().__init__()
        pygame.display.init()
        pygame.freetype.init()

        self.time = TimeInput()
        # Screen
        self.__canvases = []
        # Events
        self.events = []
        # Coroutines
        self.__coroutines = set()\

    def first_update(self):
        self.events = pygame.event.get()
        root.update_mouse_position()

        # update_behaviour = [(False or True)]
        if update_behaviour[0]:
            root.update_virtual_behaviour()
            update_behaviour[0] = False

        self.time.update()

    def last_update(self):
        self.run_coroutine()
        pygame.display.update()

    def start_coroutine(self, coroutine):
        self.__coroutines.add(coroutine)

    def __run_and_check_delete_coroutine(self):
        # Giá trị đầu tiên trả ra là True hoặc False
        # Nếu True : có một coroutine kết thúc
        # Nếu False : không có coroutine nào kết thúc -> không cần xóa tập coroutines
        # Việc này tránh tính toán lại tập coroutine ở mỗi frame
        checked = False

        for coroutine in self.__coroutines:
            try:
                coroutine.__next__()
            except StopIteration:
                # Chặn điều kiện -> giá trị đầu tiên luôn là là 'bool'
                if not checked:
                    checked = True
                    yield True
                yield coroutine
        yield False

    def run_coroutine(self):
        if not self.__coroutines:
            return

        generator_ = self.__run_and_check_delete_coroutine()
        # Kiểm tra giá trị đầu tiên
        if generator_.__next__():
            self.__coroutines = self.__coroutines.difference(generator_)

    @classmethod
    def quit(cls):
        pygame.quit()
        sys.exit()

app = GameSystem()

class SpecialCoroutine:
    @staticmethod
    def wait(second_time_wait):
        count_time = 0

        while count_time < second_time_wait:
            count_time += app.time.delta_time
            yield None

    @staticmethod
    def lerp(__from, __target, __second_time):
        __distance = float(__target - __from)
        __speed = __distance / __second_time
        count_time = 0

        while count_time < __second_time:
            count_time += app.time.delta_time

            __remember = __from.copy()
            __from.lerp(__target, __speed * app.time.delta_time)
            yield __from - __remember

