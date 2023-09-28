<h1 align="center">🐍 PYXEL 1.0.0 🐍</h1>

<h1 align="center">🎮 Giới thiệu 🎮</h1>
<img align="right" width="256px" height="256px" src="https://github.com/Ca-Len-Men/Pyxel/assets/88229844/e1bbdbd5-18ee-41e7-9994-b0d958d089c5">

### Về thư viện `PYXEL`
- `PYXEL` là thư viện <u>mã nguồn mở</u> được xây dựng dựa trên `Pygame`, hoạt động trên tinh thần lắng nghe ý kiến người dùng, hợp tác và cùng phát triển.
- `PYXEL` mong muốn cung cấp nhiều tiện ích, tính năng cho phát triển trò chơi 2D với lập trình viên :
	- Dễ dàng sử dụng cho người mới học.
	- Cung cấp các mẫu điều khiển đẹp mắt.
	- Hỗ trợ tận tình cho lập trình viên từ A đến Z khi nhận được phản hồi.
- Thông tin đến các ***cộng tác viên*** :
	- Chi tiết về `pyxel` : [REVIEW.md](beta/pyxel/REVIEW.md)
	- Chi tiết về `cyxelclec` : Updating...

### Trước khi bắt đầu, `PYXEL` yêu cầu bạn :
* Đã cài đặt gói `pygame`, `numpy` 📦 ( <b>bắt buộc</b> ).
* Bạn hãy lựa chọn một trong hai gói sau để tải về :
	- Phiên bản Pure Python : ~~chưa hoàn thành~~ ...
	- Phiên bản Cython		: ~~chưa hoàn thành~~ ...
	- <b>Lưu ý</b> : đối với phiên bản Cython, `PYXEL` đòi bạn cài thêm gói `Cython` và thực thi tệp `setup.py` mới có thể sử dụng.

## <h1 align="center">⛓️ Mô hình Canvas Layer - Entity - Component ⛓️</h1>

> Vì cảm thấy mô hình này phù hợp với tình hình hiện tại, nếu độc giả có góp ý chỉnh sửa, hoặc có ý tưởng sửa đổi phù hợp hơn, xin hãy liên hệ cho tôi 😊. Thank you so much !

<details>
<summary><h3>Đối tượng <code>Canvas</code></h3></summary>

- Là khu vực dùng để hiển thị các đối tượng bên trong nó ( hãy xem nó như một màn hình, các đối tượng bên trong không thể được hiển thị ra bên ngoài màn hình ).
- Chúng ta sẽ đặt ra các quy tắc để dễ dàng làm việc với nhau :
	- [PYXEL1](#PYXEL1) : Một `Canvas` có thể chứa nhiều `Canvas` khác.
	- [PYXEL2](#PYXEL2) : Dựa vào `PYXEL1`, ta có một <u>cây</u> gồm các nút là các `Canvas`, với nút gốc ( `root` ) chính là toàn màn hình của ứng dụng.
</details>

---

<details>
<summary><h3>Đối tượng <code>Entity</code></h3></summary>

- Là "định danh" cho một "thực thể" bên trong trò chơi :
	- [PYXEL3](#PYXEL3) : Một `Canvas` có thể chứa nhiều `Entity`.
</details>

---

<details>
<summary><h3>Đối tượng <code>Component</code></h3></summary>

- Là các "thành phần" được gắn vào một và chỉ một `Entity`, các `Component` bên trong liên kết hoàn chỉnh thành một "thực thể" :
	- [PYXEL4](#PYXEL4) : Một `Entity` có thể chứa nhiều `Component`.
	- [PYXEL5](#PYXEL5) : Tùy vào loại `Component`, mà có thể có nhiều `Component` <u>cùng loại</u> cùng gắn trên một `Entity`, hoặc <u>chỉ một loại</u> `Component` được gắn trên `Entity` đó.
	- [PYXEL6](#PYXEL6) : `Entity` chỉ có chức năng lưu trữ `Component`, không thể được phép kế thừa hoặc mở rộng.
</details>

## <h1 align="center">⛓️ Sản phẩm ⛓️</h1>

> Cùng điểm qua một số sản phẩm nhỏ được tạo bằng `PYXEL` nhé 😊

### Trang đăng nhập, đăng ký đơn giản, đẹp mắt.

https://github.com/Ca-Len-Men/Extensions-for-Pygame-Vietdoc/assets/88229844/efd72a2b-c649-4910-ae1b-22a74b91a277

