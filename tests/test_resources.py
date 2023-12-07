import env
import json
import resources
from loguru import logger


wftxt = """{
    "user": "laogao",
    "dowhat": "test"
}"""
wfjs = {
    "user": "laogao",
    "dowhat": "test"
}
class TestObject:
    a = 1
tobj = TestObject()
tobj.a = 114514

# use resources create file and dir
resources.get("tests").create("test.json", wftxt).as_text()
resources.get("tests").create("test.json", wfjs).as_json()
resources.get("tests").create("bytesFile.pyc", tobj).as_object()
resources.get("tests").create("child_dir/file.test", "test file").as_text()

# return src/tests/test.json
p = resources.get("tests").path("test.json")
logger.info(p)

# return "{ "laogao": "1234" }" -> str
txt = resources.get("tests").load("test.json").text
logger.info(txt + " - type: " + type(txt).__name__)

# return { "laogao": "1234" } -> _Dict
dc = resources.get("tests").load("test.json").json
logger.info(str(dc) + " - type: " + type(dc).__name__)

# join child dir
ctxt = resources.get("tests/child_dir").load("file.test").text
logger.info(ctxt)

obj = resources.get("tests").load("bytesFile.pyc").Object
logger.info(obj.a)

# add extension
def load_json_as_list(f_obj: resources.File):
    with open(resources.base.join(f_obj.path), "r") as file:
        data: dict = json.load(file)
    return [(key, value) for key, value in data.items()]
    
resources.extension.add("list_json", load_json_as_list, _property=True)
data = resources.get("tests").load("test.json").list_json
logger.info(str(data))