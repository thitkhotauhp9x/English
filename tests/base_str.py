from collections import UserDict
from typing import Self

from pydantic import BaseModel


class ChainStr(BaseModel):
    content: str

    def __str__(self):
        return self.content

    def __repr__(self):
        return str(self)

    def __or__(self, other):
        return f"{str(self)}{str(other)}"


class dfd(UserDict):
    ...

class Rule(BaseModel):
    id: str
    title: str
    description: str


class RuleCollection(BaseModel):
    rules: list[Rule]

    def __add__(self, other: Rule) -> Self:
        self.rules.append(other)
        return self

    def __str__(self):
        content = "\n".join([f"- {rule.id} {rule.title} {rule.description}" for rule in self.rules])
        return f"""
Rules
====
{content}
"""


collection = RuleCollection()
collection += Rule()

class Rules(ChainStr):
    content: str

    def __str__(self):
        return f"""
Rules
===
{self.content}
"""


query = ChainStr(content="Compute the length of the string.")
# query |= Rules(content="- Hello you")
query |= RuleCollection() + Rule() + Rule()


print(query)
