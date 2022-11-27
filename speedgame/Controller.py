__doc__ = '''           Ngày tạo : 16/11/2022
File Controller.py  : định nghĩa các lớp Design Pattern, giải quyết một vấn đề nhất định.
'''

import sys
import inspect
import json
from typing import List, Dict, Union, Any
from abc import ABC, abstractmethod
from random import randint
from speedgame.Handle import SingletonMeta, app

__version__ = '1.0.0'


class ExistenceController:
    """Class **ExistenceController** : quản lí tạo và giải phóng các *GameObject*."""

    __doc__ = 'Class ExistenceManager : quản lý sự tồn tại của các GameObject và giải phóng nó khi không dùng tới.'

    class IGameObject(ABC):

        __doc__ = 'Class IGameObject : interface cho các lớp muốn sử dụng lớp ExistenceController kế thừa.'

        # Phương thức destroy : trả về true cho biết GameObject này không cần dùng nữa ( giải phóng ).
        @abstractmethod
        def destroy(self) -> bool: pass

        # Phương thức update : cập nhật GameObject trên từng khung hình.
        @abstractmethod
        def update(self, action) -> None: pass

    def __init__(self, limit=1000):
        """ Khởi tạo lớp **ExistenceController**.

        :param limit: giới hạn số lượng tạo GameObject.
        """

        self.list_object = {}
        self._limit = limit

    def update(self, action=True):
        """ Phương thức **update** : cập nhật, quản lý các *GameObject*.

        :return: None
        """

        keys_destroy = []
        for key, value in self.list_object.items():
            value.update()
            if value.destroy():
                keys_destroy.append(key)

        for key in keys_destroy:
            del self.list_object[key]

    def add(self, game_object: IGameObject):
        """ Phương thức **add** : thêm một *GameObject*.

        :param game_object: GameObject cần thêm vào.
        :return: None
        """

        # Đạt giới hạn số lượng GameObject.
        if len(self.list_object) == self._limit:
            return

        while True:
            key = randint(-self._limit, self._limit)
            if key not in self.list_object:
                break
        self.list_object[key] = game_object


class SceneController(metaclass=SingletonMeta):
    """Class **SceneController** : *SceneController Design Pattern*, quản lí các phân cảnh trò chơi."""

    class IScene(ABC):
        """Lớp **IScene** : quản lý một phân cảnh trò chơi."""

        __doc__ = ''' Lớp IScene : lớp tổng quát cho các scene kế thừa.
            Định nghĩa các phương thức của IScene để SceneController biết nó phải làm thế nào.
            SceneController sẽ tự động tìm đến các lớp kế thừa IScene, khởi tạo một thể hiện và thực thi nó.
            (*) Tất cả các lớp kế thừa IScene đều phải được viết trong cùng một module *.py !
            '''

        def __new__(cls, *args, **kwargs):
            instance = super(SceneController.IScene, cls).__new__(cls)

            # Mỗi phân cảnh sẽ chứa các dữ liệu cần thiết để thực thi phân cảnh đó.
            # Sau khi chuyển sang phân cảnh khác, những dữ liệu còn sử dụng hãy giữ vào hai biến args, kwargs.
            # Để cho SceneController gửi chúng sang phân cảnh mới ( bằng cách truyền như tham số khi khởi tạo ).
            # (*) Phân cảnh đầu tiên không được có tham số ( trừ những tham số mặc định ) !
            # Biến prev_scene cho biết phân cảnh nào trước đó vừa gọi đến nó.
            # Biến end_scene cho biết liệu phân cảnh này đã kết thúc chưa.
            # Biến goto_scene cho biết sẽ đi đến phân cảnh nào tiếp theo.
            instance.end_scene = False
            instance.goto_scene = ''
            instance.args = list(args)
            instance.prev_scene = kwargs['PREV_SCENE']
            instance.kwargs = kwargs
            return instance

        @abstractmethod
        def update(self) -> None:
            """ Phương thức **update** : cập nhật phân cảnh trên từng khung hình.

            :return: None
            """

        def end(self, scene_name: str):
            """ Phương thức **end** : kết thúc phân cảnh, chuyển sang phân cảnh có tên *scene_name*.

            :param scene_name: Tên của lớp kế thừa SceneController.IScene.
            :return: None
            """

            self.end_scene = True
            self.goto_scene = scene_name

    __doc__ = ''' Lớp SceneController : quản lý chuyển đổi các phân cảnh trong trò chơi.
        Các scene kế thừa lớp IScene, một cách tự động SceneController sẽ chuyển đổi qua lại giữa cách phân cảnh.'''

    def __init__(self, module_name: str, first_scene: str):
        """ Phương thức **__init__** : khởi tạo các thông số cho *SceneController*.

        :param module_name: Tên của module định nghĩa các lớp kế thừa SceneController.IScene.
        :param first_scene: Tên của lớp thực hiện phân cảnh đầu tiên khi trò chơi bắt đầu.
        """

        self.scenes = SceneController.__search_class(module_name)
        assert first_scene in self.scenes, 'Không tìm thấy tên của lớp đã kế thừa IScene !'

        self.__present_scene: SceneController.IScene = self.scenes[first_scene](*(), **{'PREV_SCENE': None})

    def run(self):
        """ Phương thức **run** : thực thi các phân cảnh, chuyển phân cảnh của trò chơi.

        :return: None
        """

        while True:
            self.__present_scene.update()

            # Chuyển phân cảnh
            if self.__present_scene.end_scene:
                app.cursor.refresh()
                name_next_scene = self.__present_scene.goto_scene

                # Thêm khóa 'PREV_SCENE' làm tham số.
                self.__present_scene.kwargs['PREV_SCENE'] = self.scenes[name_next_scene]
                next_scene = self.scenes[name_next_scene](*self.__present_scene.args, **self.__present_scene.kwargs)

                # Lưu phân cảnh tiếp theo
                self.__present_scene = next_scene

            app.update()

    @staticmethod
    def __search_class(module_name: str):
        """ Phương thức **__search_class** : tìm các lớp kế thừa *SceneController.IScene*.

        :param module_name: Tên module định nghĩa các lớp kế thừa SceneController.IScene.
        :return: Dict[str, class] của các lớp mà nó tìm thấy.
        """

        assert module_name in sys.modules, 'Thông báo từ lớp SceneController : module_name không tồn tại !'

        # Lấy ra cặp (tên lớp: str, lớp: class) từ các lớp kế thừa IScene trong module có tên 'module_name'.
        result = inspect.getmembers(sys.modules[module_name],
                                    lambda obj: inspect.isclass(obj) and obj.__base__ is SceneController.IScene)
        return {k: v for k, v in result}


class LayerController:
    """Class **LayerController** : *LayerController Design Pattern*, quản lý các tầng hiển thị."""

    __doc__ = '''Class LayerController : quản lý điều khiển các tầng hiển thị.
                Nhận một chuỗi json chỉ định điều khiển các tầng trong một phân cảnh.'''

    def __init__(
        self,
        json_control: str,
        dict_gameobjects: Dict[str, Union[Any, List[Any]]],
        layer_name: str
    ):
        # gameobjects : dictionary chứa các cặp (tên của GameObject, GameObject)
        self.gameobjects = dict_gameobjects

        # layer_name : khóa của layer sẽ được thực thi.
        self.layer_name = layer_name

        # layers: Dict[layer_name: str, List[List[ordered: int, gameobject_name: str, action: bool]]].
        # Các GameObject sẽ thực thi theo thứ tự ordered tăng dần.
        self.layers = json.loads(json_control)
        for layer in self.layers.values():
            layer.sort()      # Sắp xếp tăng dần theo ordered

    def update(self):
        """ Phương thức **update** : thực thi các tầng đã định nghĩa trong một phân cảnh.

        :return: None
        """

        assert self.layer_name in self.layers, 'Layer name không tồn tại !'

        # Thực thi các GameObject có tên trong layer.
        for tup in self.layers[self.layer_name]:
            assert tup[1] in self.gameobjects, f'Key {tup[1]} doesn\'t exists !'
            ref = self.gameobjects[tup[1]]
            if type(ref) is list:
                for game_object in ref:
                    game_object.update(tup[2])
            else:
                ref.update(tup[2])
