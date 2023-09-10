from abc import ABC

class Singleton(ABC):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

class Static(ABC):
    def __new__(cls, *args, **kwargs):
        raise ValueError(f"From {cls.__name__}.__init__ : "
                         f"can't initalize instance of static class !")