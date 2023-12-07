# 这个文件控制资源，让其他文件更好的加载所需文件

"""
应该的用法
```python
import resources

# return src/configs/user.config
resources.get("configs").path("user.config")

# return "{ "laogao": "1234" }" -> str
resources.get("configs").load("user.config").text

# return { "laogao": "1234" } -> _Dict
resources.get("configs").load("user.config").json

# join child dir (12345 is server's id, 5231 is user's id)
resources.get("server-meta/12345/5231").load("data.json").json

# load object(pickle)
resources.get("objects").load("data.pyc").Object

# add other method
def load_json_as_list(file_name: str) -> List[str | int]:
    with open(resources.base.join(file_name), "r") as file:
        data: _Dict = json.load(file)
    return [(key, value) for key, value in data.items()]
    
resources.extension.add("list_json", load_json_as_list, _property=True, _async=False)
resources.get("configs").load("userdata.json").list_json
```
1.base类:
    i.   其中有一个值为 _CONST_BASE 为src的完整路径
    ii.  base值是动态的, 他应该因为resources.get方法而变动
    iii. 在加载完成后必须恢复 base, 或是每次使用 get 时恢复base
"""
import os as _os
import json as _json
import os.path as _path
import pickle as _pickle
import inspect as _inspect
from typing import Dict as _Dict
from typing import Callable as _Callable


_DIR = _path.dirname(_path.dirname(_path.abspath(__file__)))
_SRC = _path.join(_DIR, "src")



class base:
    _CONST_BASE = _SRC
    _base = _CONST_BASE
    @staticmethod
    def join(file_path: str) -> str:
        return _path.join(base._base, file_path)

class _Directory(object):
    def __init__(self, dirpath: str) -> None:
        self.dirpath: str = dirpath
    
    def load(self, filename: str) -> "_File":
        return _File(_path.join(self.dirpath, filename))
    
    def path(self, filename: str) -> str:
        return _path.join(self.dirpath, filename)

    def create(self, filename: str, obj) -> "_SaveFile":
        path: str = _path.join(self.dirpath, *filename.split("/"))
        _os.makedirs(_path.dirname(path), exist_ok=True)
        return _SaveFile(path, obj)
    
class _SaveFile:
    def __init__(self, filepath: str, content: str) -> None:
        self.filepath = filepath
        self.content = content
    

    def as_text(self):
        with open(self.filepath, "w") as fp:
            fp.write(self.content)
        
    def as_json(self):
        with open(self.filepath, "w") as fp:
            _json.dump(self.content, fp)
    
    def as_object(self):
        with open(self.filepath, "wb") as fp:
            _pickle.dump(self.content, fp)

class _File(object):
    def __init__(self, filepath: str) -> None:
        self.path = filepath

    @property
    def text(self):
        with open(self.path, "r") as file:
            text = file.read()
        return text
    @property
    def json(self):
        with open(self.path, "r") as file_json:
            data: _Dict = _json.load(file_json)
        return data
    
    @property
    def Object(self) -> object:
        with open(self.path, "rb") as fb:
            obj: object = _pickle.load(fb)
        return obj
    
def get(_dir: str) -> _Directory:
    # reset base
    base._base = base._CONST_BASE
    # join new dir
    base._base = _path.join(base._base, *_dir.split("/"))
    return _Directory(base._base)

def create_root(name: str) -> _Directory:
    # reset base
    base._base = base._CONST_BASE
    # join
    base._base = _path.join(base._base, name)
    _os.mkdir(base._base)
    return _Directory(base._base)

class extension:
    @staticmethod
    def add(name: str, method: _Callable, _property: bool = True, _async: bool = False):
        if _async and _inspect.isasyncgenfunction(method):
            raise AttributeError("this method is not async function, please set `_async` argument as False")
        
        if _property:
            method = property(method, None, None)
        setattr(_File, name, method)

# this classes for argument type, `file: resources.File`
class File:
    def __init__(self) -> None:
        self.path: str  # file's path

__all__ = ["extension", "get", "base", "File"]