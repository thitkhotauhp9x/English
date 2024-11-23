import pdb

from langchain_core.tools import tool
import os
from langchain_openai import ChatOpenAI
from pydantic import SecretStr


@tool
def multiply(a: int, b: int) -> int:
    """
    Multiple two numbers.
    """
    return a * b

@tool
def add(a: int, b: int) -> int:
    """
    Add two numbers.
    """
    return a + b


tools = [add, multiply]


llm = ChatOpenAI(model="gpt-4o-mini", api_key=SecretStr(os.environ["OPENAI_API_KEY"]))

llm_with_tools = llm.bind_tools(tools)

pdb.set_trace()
query = "What is 3 * 12? Also, what is 11 + 49"

print(llm_with_tools)
result = llm_with_tools.invoke(query)
print(result)