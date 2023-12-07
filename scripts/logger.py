import os.path as _path
from resources import _DIR
from typing import Tuple as _Tuple

_LOGS_PATH = _path.join(_DIR, "logs")
INFO = "[INFO]"
WARNING = "[WARNING]"
ERROR = "[ERROR]"

def log(*content: _Tuple[str], level: str = INFO, sep: str= "", log_name: str = "main.log") -> None:
    content_list = [str(cstr) for cstr in content]
    info: str = level + ": " + sep.join(content_list)
    with open(_path.join(_LOGS_PATH, log_name), "a") as file:
        file.write(info + "\n")