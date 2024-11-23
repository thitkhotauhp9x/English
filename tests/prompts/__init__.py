import os
from dataclasses import dataclass

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, model_validator


@dataclass
class Rule:
    id: str
    title: str
    content: str


def get_length(value: str) -> int:
    length = 0
    for i in range(0, len(value)):
        print(i, value[i])
        length += 1
    return length

class Node(BaseModel):
    value: str
    minLength: int = 50
    maxLength: int = 52

    @model_validator(mode="after")
    def validate(self):
        print(self.model_dump_json(indent=2))
        print(self.value, len(self.value))
        if len(self.value) > self.maxLength:
            raise ValueError("Value is too long.")
        if len(self.value) < self.minLength:
            raise ValueError("Value is too short.")
        return self



def ask(query: str) -> str:
    content = f"""
Perform the following steps and give the results of each step.
- Step 1: Set minLength=10 and maxLength=12
- Step 2: Create a value with the theme of a home address that has a length greater than or equal
          to minLength and less than maxLength.
          Sử dụng thuật toán sau để tính toán chiều dài của chuỗi.
          >>> def get_length(value: str) -> int:
          >>>     length = 0
          >>>     for i in range(0, len(value)):
          >>>         print("debug", i, value[i])
          >>>         length += 1
          >>>     return length
          Nếu chuỗi có chiều dài không hợp lệ hãy tạo lại chuỗi cho đến khi nhận được kết quả hợp
          lệ.
          Nhớ đưa ra kết quả của từng bước nhỏ trong step này.
- Step 3: Sử dụng thuật toán sau để tính toán chiều dài của chuỗi value vừa tạo. 
          Nhớ thực hiện từng bước và đưa ra kết quả cuối cùng khi thực hiện thuật toán này.
          >>> def get_length(value: str) -> int:
          >>>     length = 0
          >>>     for i in range(0, len(value)):
          >>>         print("debug", i, value[i])
          >>>         length += 1
          >>>     return length

- Step 4: Generate a JSON output for the values created above: value, minLength, and maxLength.
"""

    model = ChatOpenAI(temperature=0, api_key=os.environ["OPENAI_API_KEY"])
    result = model.invoke([
        HumanMessage(content=content)
    ])
    return result.content


def main():
    # print(json.dumps(Node.model_json_schema(), indent=2))
    result = ask(query="Create data for a node.")
    print(result)
    # print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    # l = get_length("123 Main Street, City, State, Zip Code")
    # print("Result", l)
    main()
