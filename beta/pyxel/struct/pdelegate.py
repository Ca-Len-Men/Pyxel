# /**************************************************************************/
# /*  pdelegate.py                                                          */
# /**************************************************************************/
# /*                         This file is part of:                          */
# /*                                 PYXEL                                  */
# /*                  https://github.com/Ca-Len-Men/Pyxel                   */
# /**************************************************************************/

from weakref import WeakKeyDictionary
from typing import *

class Delegate:
    """ Lớp Delegate
    - Lưu nhiều các cặp key-value là (obj, callable).
    - khi sự kiện xảy ra, gọi đến tất cả các callable đó : callable(obj, sender).
    - Bất kỳ obj nào bị giải phóng, callable tương ứng cũng bị xóa khỏi dict.
    """

    def __init__(self):
        self._weak_key: Optional[WeakKeyDictionary[Any, Callable[[Any, Any], None]]] = None

    def call(self, sender: Any) -> None:
        """ Thực thi các *function* với tham số **obj, sender**.

        - ``Delegate.__call__`` chỉ được gọi khi một sự kiện xảy ra.
        :param sender: là đối tượng giữ `Delegate` này.
        """

        if self._weak_key is None:
            return

        for __obj, __function in self._weak_key.items():
            __function(__obj, sender)

    def add(self, __obj, __function: Callable[[Any, Any], None]) -> None:
        if self._weak_key is None:
            self._weak_key = WeakKeyDictionary()
        self._weak_key[__obj] = __function

    def remove(self, __obj) -> bool:
        """ Xóa **__obj** và **__function__ khỏi ``WeakKeyDictionary``.
        :return: True nếu tồn tại __obj và xóa thành công
        """

        if __obj in self._weak_key:
            del self._weak_key[__obj]
            return True
        return False
