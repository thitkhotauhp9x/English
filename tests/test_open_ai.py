import json
import logging
import os
from collections import UserDict
from dataclasses import dataclass, field
from functools import cached_property
from typing import Annotated, Type, Optional
from typing import List, Any

from langchain.output_parsers import PydanticOutputParser
from langchain_core.exceptions import OutputParserException
from langchain_core.outputs import Generation
from langchain_core.prompts import PromptTemplate
from langchain_core.utils.pydantic import TBaseModel
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, SecretStr, Field

logger = logging.getLogger(__name__)


class Dictionary(UserDict):
    def to_compact_json_string(self) -> str:
        return json.dumps(self.data, ensure_ascii=False, separators=(',', ':'))

    def delete_items_recursive(self, key: str) -> None:
        self._delete_items_recursive(self.data, key)

    @classmethod
    def _delete_items_recursive(cls, collection, key: str) -> None:
        if isinstance(collection, dict):
            if key in collection.keys():
                del collection[key]
            for _, value in collection.items():
                cls._delete_items_recursive(value, key)
        elif isinstance(collection, list):
            for component in collection:
                cls._delete_items_recursive(component, key)
        else:
            pass


class LitePydanticOutputParser(PydanticOutputParser):
    def get_format_instructions(self) -> str:
        reduced_schema = self.pydantic_object.model_json_schema()

        if "type" in reduced_schema:
            del reduced_schema["type"]

        dictionary = Dictionary(reduced_schema)
        dictionary.delete_items_recursive(key="title")
        schema_str = dictionary.to_compact_json_string()
        return _PYDANTIC_FORMAT_INSTRUCTIONS.format(schema=schema_str)

    def parse_result(
        self, result: list[Generation], *, partial: bool = False
    ) -> Optional[TBaseModel]:
        try:
            json_object = super().parse_result(result)
            print(json_object)
            return self._parse_obj(json_object)
        except OutputParserException as e:
            if partial:
                return None
            raise e

_PYDANTIC_FORMAT_INSTRUCTIONS = """The output should be formatted as a JSON instance that conforms to the JSON schema below.

As an example, for the schema {{"properties":{{"foo":{{"title":"Foo","description":"a list of strings","type":"array","items":{{"type":"string"}}}}}},"required":["foo"]}}
the object {{"foo":["bar","baz"]}} is a well-formatted instance of the schema. The object {{"properties":{{"foo":["bar","baz"]}}}} is not well-formatted.

Here is the output schema:
```
{schema}
```"""  # noqa: E501


@dataclass(frozen=True)
class CustomChatOpenAI:
    api_key: SecretStr = field(default=os.environ["OPENAI_API_KEY"])
    temperature: float = field(default=0)

    @cached_property
    def get_chat_open_ai(self) -> ChatOpenAI:
        return ChatOpenAI(temperature=self.temperature, api_key=self.api_key)

    def invoke(self, query: str, pydantic_object: Type[BaseModel]) -> BaseModel:
        parser = PydanticOutputParser(pydantic_object=pydantic_object)

        prompt = PromptTemplate(
            template="{query}\n{format_instructions}\n",
            input_variables=["query"],
            partial_variables={
                "format_instructions": parser.get_format_instructions()
            },
        )

        chain = prompt | self.get_chat_open_ai | parser
        return chain.invoke({"query": query})



class Node(BaseModel):
    label: str
    id: str


class Edge(BaseModel):
    source: Annotated[str, Field(json_schema_extra={
        "pattern": {"$data": "1/nodes/id"},
    })]
    target: str


class Flowchart(BaseModel):
    description: str
    nodes: List[Node]


class Query(BaseModel):
    instruction: str
    rules: List[Any]


class ClassName(BaseModel):
    name: str


class Student(BaseModel):
    name: str
    class_name: ClassName



from contextlib import contextmanager

@contextmanager
def accuracy(n: int):
    n_pass = 0
    n_fail = 0
    problems = []
    try:
        for _ in range(n):
            yield
        n_pass += 1
    except Exception as e:
        problems.append(e)
        n_fail += 1
    finally:
        print("N PASS::", n_pass)
        print("N FAIL::", n_fail)
        print("ACCURACY::", n_pass / (n_pass + n_fail))
        print(problems)


class TestRule:
    def test_accuracy(self, func, *args, **kwargs):
        n_pass = 0
        n_fail = 0
        for i in range(10):
            try:
                func(*args, **kwargs)
                n_pass += 1
            except Exception as e:
                logger.exception(e)
                n_fail +=1

