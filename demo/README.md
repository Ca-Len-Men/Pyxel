<h1 align="center">🐍 PYXEL DEMO 🐍</h1>

> Phần hướng dẫn này sẽ tập trung hướng dẫn các bạn tạo chức năng đầu tiên của trò chơi : đăng nhập, đăng ký, ...
> Xem video ngay bên dưới 😗

https://github.com/Ca-Len-Men/Extensions-for-Pygame-Vietdoc/assets/88229844/efd72a2b-c649-4910-ae1b-22a74b91a277

## <h1 align="center">⛓️ Trang trí Root Canvas ⛓️</h1>

> Root Canvas ( `root` ) : chính là màn hình ứng dụng của chúng ta.

- Sử dụng thư viện `PYXEL` :
```python
from pyxel import *
```

- Chỉ gồm hai bước đơn giản :
    - Tạo background : tạo một ảnh nền như trên video.
    - Tạo hiển thị FPS : được hỗ trợ bằng `ComponentScript` là `FPSDisplay`.

- Tạo ảnh nền như video :
```python
# Tạo khối 3x3 pixels.
grid = [[Dark, Dark, Dark],
        [Black, Black, Black],
        [Black, Brown, Black]
        ]

# Kéo giãn khối 3x3 cho bằng với kích thước màn hình.
surface_background = scale_grid_pixels(grid, root.rect.size)
# Khởi tạo ComponentSprite: lớp CSprite cần nhận vào một pygame.Surface
background = CSprite(surface_background)
```

- Tạo nhãn hiển thị FPS của ứng dụng :
```python
# FPSDisplay là một ComponentScript: nếu bỏ qua khóa `entity`, `FPSDisplay` tự động khởi tạo `Entity` cho nó.
fps_script = FPSDisplay(font_size=18, color=Chocolate)

# Gán `automate` của `entity` là `True`: cho phép `Entity` đó tự cập nhật mà không cần gọi phương thức `update`.
fps_script.entity.automate = True

# Hiển thị nhãn FPS ở góc phải bên trên ứng dụng: mỗi Entity, Canvas luôn có property `rect`, dùng để xác định vị trí, kích thước đối tượng.
fps_script.entity.rect.topright = root.rect.topright - Vector(15, -15)
```

- Mã hoàn chỉnh, có thể thực thi được :
```
from pyxel import *

# Tạo một lớp Scene bằng cách đánh dấu decorator `@SceneController.marked_scene` và lớp phải kế thừa từ `IScene`.

@SceneController.marked_scene
class SignInScene(IScene):
    def __init__(self, args: list, kwargs: dict):
        # Tạo Entity
        _entity = Entity()

        # Tạo ảnh nền ứng dụng
        grid = [[Dark, Dark, Dark],
                [Black, Black, Black],
                [Black, Brown, Black]
                ]
        self.sprite_background = CSprite(scale_grid_pixels(grid, root.rect.size))

        # Vì CSprite là một Component, cần thêm nó vào một Entity.
        _entity.add_component(self.sprite_background)

        # Tạo FPSDisplay: mặc định FPSDisplay tự khởi tạo Entity cho chính nó.
        self.fps_script = FPSDisplay(font_size=18, color=Chocolate)
        self.fps_script.entity.automate = True
        self.fps_script.entity.rect.topright = root.rect.topright - Vector(15, -15)

        # Tấn tần tật mọi thứ đều là con/cháu của `root`
        # Thêm các Entity vào `root`
        root.add_entities(_entity, self.fps_script.entity)
    
    # Phương thức `update` của `IScene`: được gọi mỗi khung hình.
    def update(self, args: list, kwargs: dict):
        # Vẽ ảnh nền lên trước những thứ khác
        self.sprite_background.update()

        # Cập nhật root: nếu có bất kì `entity.automate` nào là True, buộc phải gọi `root.update()` để tránh bỏ sót chúng.
        # Nếu không có, bạn có thể không cần dòng này.
        root.update()

if __name__ == '__main__':
    # Khởi tạo ứng dụng thông qua `app`
    # Kích thước ứng dụng là 1200x790, với caption là `Demo`
    app.init((1200, 790), 'Demo')

    # Cho phép ứng dụng chỉ khởi chạy 30 khung hình trên mỗi giây
    # Nếu không chỉ định con số này, mặc định ứng dụng sẽ dốc toàn lực của nó.
    app.time.fps = 30

    # Khởi tạo lớp quản lí scene, và bắt đầu với scene `SignInScene`.
    scene_controller = SceneController('SignInScene')
    scene_controller.run()

```
