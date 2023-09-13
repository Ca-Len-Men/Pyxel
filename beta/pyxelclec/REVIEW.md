<h1 align="center">🐍 PYXEL 1.0.0 REVIEW 🐍</h1>


<h1 align="center">🎮 Giới thiệu sơ đồ 🎮</h1>
<img align="right" width="256px" height="256px" src="../../Assets/code-review.png">

### Cây thư mục

```
pyxelclec
+----geo
|       \   __init__.py
|       \   fmath.py
|       \   fvector.py
|       \   frect.py
|       \   fdraw.py
|       \   color.py
|       \   imagine.py
|
+----model
|       +----components
|       |       \   __init__.py
|       |       \   ccollider.py
|       |       \   cinput.py
|       |       \   cscripts.py
|       |       \   csprite.py
|       |
|       \   __init__.py
|       \   component.py
|       \   entity.py
|       \   canvas.py
|       \   base.py
|
+----scripts
|       \   __init__.py
|       \   timing.py
|       \   button.py
|       \   text.py
|
\   __init__.py
\   __flag__.py
\   __info__.py
\   assets.py
\   pattern.py
\   scene.py
```

---

<h1 align="center">📑 Giới thiệu <code>pyxelclec.geo</code> 📑</h1>

### Module `fmath.py`

- Các hàm tính toán :

| Các biến và hàm | Chức năng | Ghi chú |
|:--------------|:---------:|:--------|
| APPROXIMATE = 0.000_000_001 | Sai số có thể chấp nhận | |
| PI = 3.14159_26535_89793 | Giá trị xấp xỉ của `pi` | |
| **def** _radians(`__degrees`: *float*) -> *float* | Đổi từ `degrees` sang `radians` | |
| **def** _degrees(`__radians`: *float*) -> float | Đổi từ `radians` sang `degrees` | |
| **def** relative_compare(`a`: *float*, `b`: *float*) -> *bool* | So sánh bằng hai kiểu `float` | `abs(a - b) <= APPROXIMATE` thì được xem là `a == b` |
| **def** angle(`vec_x`: *float*, `vec_y`: *float*) -> *float* | Tính góc của `vector(x, y)` | Giá trị trả về trong đoạn `[0, 360]` |
| **def** vector(`__degrees`: *float*) -> Tuple[*float*, *float*] | Trả về giá trị `x, y` của `vector` độ dài `1` có góc bằng `__degrees` | |
| **def** magnitude(`x`: *float*, `y`: *float*) -> *float* | Tính độ dài `vector(x, y)` | |
| **def** lerp(`current`: *float*, `target`: *float*, `delta`: *float*) -> *float* | Tịnh tiếng từ `current` đến `target` một khoảng `delta` | |

### Module `fvector.py`

- Updating ...

### Module `frect.py`

- Updating ...

### Module `fdraw.py`

- Updating ...

### Module `color.py`

- Updating ...

### Module `imagine.py`

- Updating ...
