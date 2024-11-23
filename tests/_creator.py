import json
from textwrap import indent

from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field, model_validator
from uuid import UUID
from typing import List, Self, Optional, Any, Annotated

from search.example import Flowchart


class Node(BaseModel):
    content: str
    id: str


class Edge(BaseModel):
    source: str
    target: str


class FlowChart(BaseModel):
    nodes: List[Node]
    edges: List[Edge]


def main():
    model = ChatOpenAI(temperature=0)
    parser = PydanticOutputParser(pydantic_object=FlowChart)

    prompt = PromptTemplate(
        template="{format_instructions}\n{query}\n",
        input_variables=["query"],
        partial_variables={
            "format_instructions": parser.get_format_instructions()
        },
    )

    chain = prompt | model | parser
    joke_query = "Create a flowchart to 5 nodes có dùng id"

    result = chain.invoke({"query": joke_query})
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
    # print(json.dumps(Node.model_json_schema(), indent=2))
