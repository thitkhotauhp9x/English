from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from typing import List, Any


@tool
def add(a: int, b: int) -> int:
    """Adds a and b.

    Args:
        a: first int
        b: second int
    """
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """Multiplies a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b


tools = [add, multiply]
llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools(tools)

query = "What is 3 + 4 * 15"
messages: List[Any] = [HumanMessage(query)]
ai_msg = llm_with_tools.invoke(messages)
print(ai_msg.content)
messages.append(ai_msg)

for tool_call in ai_msg.tool_calls:
    selected_tool = {"add": add, "multiply": multiply}[tool_call["name"].lower()]
    tool_output = selected_tool.invoke(tool_call["args"])
    result = ToolMessage(tool_output, tool_call_id=tool_call["id"])
    print(result)
    messages.append(result)

print(messages)


