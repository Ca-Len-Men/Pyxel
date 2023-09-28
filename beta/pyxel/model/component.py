# /**************************************************************************/
# /*  component.py                                                          */
# /**************************************************************************/
# /*                         This file is part of:                          */
# /*                                 PYXEL                                  */
# /*                  https://github.com/Ca-Len-Men/Pyxel                   */
# /**************************************************************************/

"""
Component là các thành phần tạo nên một GameObject trong trò chơi.
Ví dụ : một nhân vật gồm nhiều component như cánh tay, chân, thân, đầu.

Các Component được gôm vào một Entity để tạo nên một thực thể trong trò chơi.
Component được chia ra nhiều loại cần thiết :
    - ComponentCollider : phụ trách kiểm tra va chạm, bao bọc một điểm ( vector ), ...
    - ComponentMouseInput : kiểm tra các sự kiện chuột xảy ra trên một Component,
                            phụ thuộc vào ComponentCollider.
    - ...

- Một Entity có thể lưu nhiều, hoặc chỉ một loại Component ( do Component.quantity quyết định ).
<component_class>.quantity() trả về ONLY_ONE hoặc MANY -> quyết định số lượng của chúng trong một Entity.
"""


ONLY_ONE = 0b001
MANY = 0b010

class Component:
    def __init__(self):
        self.visible = True
        self.entity = None

    def research(self, entity) -> None:
        """ Một Component có thể cần đến các Component khác để làm tốt nhiệm vụ của nó.
        Phương thức này cho phép nó tìm đến các Component khác trong Entity chứa nó.

        - Phương thức này chỉ nên được gọi thì Entity gọi hàm ``Entity.re_structure``.

        :param entity: Entity chứa self
        """
        pass

    def reset(self) -> None:
        """ Quay về trạng thái lúc ban đầu khởi tạo Component. """
        pass

    def update(self) -> None:
        """ Dành cho ``ComponentScript``, hoặc các ``Component`` cần cập nhật theo thời gian thực.

        - **(!)** : nếu ``self`` không phải ``ComponentScript``, cần hàm này trong một ``ComponentScript`` cùng chung Entity.
        :return:
        """
        pass

    def quantity(self) -> int:
        """ Số lượng tối đa Component loại này có thể thuộc một Entity. """
        return MANY

    def __hash__(self):
        return id(Component)
