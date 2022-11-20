__doc__ = '''           Ngày tạo : 19/11/2022.
File Rule.py    : định nghĩa các lớp quy chuẩn, các decorator, chúng sẽ thông báo lỗi nếu có sai phạm xảy ra.
Lớp StaticClassMeta : như tên của nó, nó muốn các lớp con kế thừa phải là tĩnh
                      ( tức là không thể khởi tạo biến ).
Lớp SingletonMeta   : nó muốn các lớp con kế thừa chỉ có thể khởi tạo một lần duy nhất.
Lớp Resource        : lưu trữ các thông tin tài nguyên của thư viện.
'''

__version__ = '1.0.0'

import os


class StaticClassMeta(type):
    __doc__ = ''' Class StaticClassMeta dành cho những lớp là tĩnh, lớp đó sẽ kế thừa từ StaticClassMeta.
                Nếu bạn vẫn khởi tạo lớp thì lỗi sẽ được xuất ra.'''

    def __call__(cls):
        assert False, f'Bạn không được phép khởi tạo lớp {cls.__name__} vì nó là lớp tĩnh !'


# Class SingletonMeta : Singleton Design Pattern, cho các lớp khác kế thừa.
class SingletonMeta(type):
    __doc__ = '''Những lớp kế thừa SingletonMeta, khi khởi tạo lớp sẽ chỉ có duy nhất một thể hiện của lớp được tạo ra.
                (*) Không được cài đặt phù hợp trong môi trường đa luồng !'''

    # Lưu một thể hiện của mỗi lớp vào biến _instance.
    # Với khóa là lớp đó và giá trị là thể hiện của lớp đó.
    _instance = {}

    # Định nghĩa lại hàm tạo lớp.
    def __call__(cls, *arg, **kwargs):
        if cls not in cls._instance:
            instance = super().__call__(*arg, **kwargs)
            cls._instance[cls] = instance
        return cls._instance[cls]


class Resource(metaclass=StaticClassMeta):
    __doc__ = 'Lớp Resource : lưu trữ thông tin các tài nguyên chuẩn của thư viện.'

    icon_dir = 'InterfaceIcons'
    font_dir = 'InterfaceFonts'
    font_name = 'JetBrains'
    font_save = {}

    # Lấy tất cả tên asset có trong folder InterfaceIcons, InterfaceFonts
    InterfaceIcons = {path[:path.index('.')]: path for path in os.listdir(icon_dir)}
    InterfaceFonts = {path[:path.index('.')]: path for path in os.listdir(font_dir)}


# Hàm load_asset : một decorator cho biết thư mục cần tìm và đuôi mở rộng của tệp tin.
def load_asset(dir_name: str):
    def decorator(load_method):
        def wrapper(self, asset_name: str):
            assert asset_name in getattr(Resource, dir_name),\
                f'Tài nguyên tên {asset_name} không tồn tại trong thư mục {dir_name} !'

            path = f'{dir_name}/{getattr(Resource, dir_name)[asset_name]}'
            return load_method(self, path)
        return wrapper
    return decorator


if __name__ == '__main__':
    pass
