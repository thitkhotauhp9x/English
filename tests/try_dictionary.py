import json5
from pydantic import BaseModel


class Student(BaseModel):
    name: str
    old: int

    # @model_validator(mode='before')
    # @classmethod
    # def validate_model(cls, data: Any) -> Any:
    #     print(data)
    #     d = json5.loads(data)
    #     return json5.dumps(d)


def try_abc():
    js = """{
"name": "b",
"old": 1,
}"""
    data = json5.loads(js)
    print(data)
    s = Student(**data)
    print(s)

try_abc()