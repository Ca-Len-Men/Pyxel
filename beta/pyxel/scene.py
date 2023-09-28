# /**************************************************************************/
# /*  scene.py                                                              */
# /**************************************************************************/
# /*                         This file is part of:                          */
# /*                                 PYXEL                                  */
# /*                  https://github.com/Ca-Len-Men/Pyxel                   */
# /**************************************************************************/

from pyxel.system_warning import warning_report
from pyxel.model.base import app
from pyxel.model.canvas import root

import pygame
from queue import Queue
from threading import Thread

class IScene:
    def __new__(cls, args, kwargs):
        instance = super().__new__(cls)
        instance.enable = True
        instance.goto_scene = ''
        instance.prev_scene = kwargs['PREV_SCENE']
        return instance

    def update(self, args, kwargs): pass

    def next(self, scene_name):
        self.enable = False
        self.goto_scene = scene_name

class ThreadTask:
    __task_queue = Queue()
    __finish_task_queue = Queue()
    _ended = False

    @classmethod
    def stop_thread(cls):
        cls.__task_queue.put(None)

    @classmethod
    def add_task(cls, __callable):
        cls.__task_queue.put(__callable)

    @classmethod
    def add_finished_task(cls, value):
        cls.__finish_task_queue.put(value)

    @classmethod
    def get_finished_task(cls):
        return cls.__finish_task_queue.get(block=True)

    @classmethod
    def have_task_finished(cls):
        return not cls.__finish_task_queue.empty()

    @classmethod
    def event_process(cls):
        # If is None, the event process will be stopped !
        # Other : result returned from task queue is callable object,
        # and call this obj will send results to finish_task_queue

        while True:
            callable_ = cls.__task_queue.get(block=True)
            if callable_ is None:
                break

            if callable(callable_):
                results = callable_()
                cls.__finish_task_queue.put(results)
            else:
                # 'callable_' is the value
                cls.__finish_task_queue.put(callable_)
        cls._ended = True

class SceneController(ThreadTask):
    __scenes = {}
    __sender_args = []
    __sender_kwargs = {'PREV_SCENE': 'START'}

    @classmethod
    def marked_scene(cls, class_):
        assert issubclass(class_, IScene), \
            f'From AsyncSceneController.wait_marked : ' \
            f'class name {class_.__name__} not derived from IScene !'

        cls.__scenes[class_.__name__] = class_
        return class_

    def __init__(self, first_scene):
        self.__current_scene_name = first_scene
        self.__current_scene = None

    def __main_process(self):
        self.__current_scene = SceneController.__scenes[self.__current_scene_name](
            SceneController.__sender_args,
            SceneController.__sender_kwargs
        )
        warning_report.checking()

        enable = True
        while enable:
            app.first_update()
            self.__current_scene.update(
                SceneController.__sender_args,
                SceneController.__sender_kwargs
            )
            app.last_update()

            for event in app.events:
                if event.type == pygame.QUIT:
                    enable = False
                    self.stop_thread()
                    pygame.quit()

            if not self.__current_scene.enable:
                next_scene = self.__current_scene.goto_scene
                del root.canvases, root.entities

                if next_scene == 'QUIT':
                    if not SceneController._ended:
                        SceneController.stop_thread()
                    break

                SceneController.__sender_kwargs['PREV_SCENE'] = next_scene
                self.__current_scene_name = next_scene
                self.__current_scene = SceneController.__scenes[self.__current_scene_name](
                    SceneController.__sender_args,
                    SceneController.__sender_kwargs
                )
                warning_report.checking()

    def _run_main_and_thread(self):
        thread = Thread(target=ThreadTask.event_process)
        thread.start()
        self.__main_process()
        thread.join()

    def run(self, __thread=False):
        if __thread:
            self._run_main_and_thread()
        else:
            self.__main_process()
