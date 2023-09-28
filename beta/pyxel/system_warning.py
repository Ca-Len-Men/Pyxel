# /**************************************************************************/
# /*  system_warning.py                                                     */
# /**************************************************************************/
# /*                         This file is part of:                          */
# /*                                 PYXEL                                  */
# /*                  https://github.com/Ca-Len-Men/Pyxel                   */
# /**************************************************************************/

from weakref import WeakSet

class SystemWarning:
    def __init__(self):
        self._enable = True
        self._weakset = WeakSet()

    def add(self, __obj):
        self._weakset.add(__obj)

    def checking(self):
        if self._enable:
            for obj in self._weakset:
                obj.warning()

    @property
    def enable(self):
        return self._enable

    @enable.setter
    def enable(self, __enable):
        self._enable = __enable

warning_report = SystemWarning()
