from functools import singledispatch
from typing import List, Any, Dict


@singledispatch
def delete(obj: Any, key: str) -> None:
    pass


@delete.register(list)
def _(obj: List[Any], key: str) -> None:
    for item in obj:
        delete(item, key)


@delete.register(dict)
def _(obj: Dict[str, Any], key) -> None:
    if key in obj.keys():
        del obj[key]

    for _, value in obj.items():
        delete(value, key)


data = {
  "properties": {
    "name": [{
       "title": "abc",
      "type": "string"
    }],
    "age": {
      "type": "integer"
    }
  },
  "required": [
    "name",
    "age"
  ],
  "title": "Student",
  "type": "object"
}

delete(data, "title")
print(data)

#
# class TestPydantic:
#     def remove_title(self, data):
#         for key, value in data.items():
#             if key == "title":
#                 del data[key]
#             if is_
#
#     def test_pydantic(self):
#         class Student(BaseModel):
#             name:str
#             age: int
#
#             class Config:
#                 @staticmethod
#                 def json_schema_extra(schema: dict[str, Any]) -> dict:
#                     if "title" in schema:
#                         del schema["title"]
#
#                     for prop in schema.get("properties", {}).values():
#                         if "title" in prop:
#                             del prop["title"]
#                     return schema
#
#         print(json.dumps(Student.model_json_schema(), indent=2)) # 66
#         # print(Student.model_json_schema()) # 43
#         # data = json.dumps(Student.model_json_schema(), separators=(',',':')) # 32
#         # print(data)
#
#     def test_2(self):
#         class Student(BaseModel):
#             name: Literal["LEE"]
#
#         class NameStudent(Enum):
#             Lee = "LEE"
#
#         class Student2(BaseModel):
#             name: NameStudent
#
#         print(Student.model_json_schema())
#         print(Student2.model_json_schema())
#
#         x = json.dumps(Student.model_json_schema())
#         print(x)
#         y = json.dumps(Student2.model_json_schema())
#         print(y)
#         ...
#
a=1
delete(a, "title")
print(a)