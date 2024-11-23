import inspect
import logging
import os
from abc import abstractmethod
from dataclasses import dataclass
from typing import List

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

logging.basicConfig(
    filemode='a',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.DEBUG
)
import logging


class PrettyLogger(logging.getLoggerClass()):
    def log(self, level, msg: str, *args, **kwargs):
        message = msg % args
        if "\n" not in message:
            super().log(level, message, **kwargs)
        else:
            parts = message.split("\n")
            for part in parts:
                super().log(level, part, **kwargs)

    def debug(self, msg: str, *args, **kwargs):
        self._pretty(super().debug, msg, *args, **kwargs)

    def info(self, msg: str, *args, **kwargs):
        self._pretty(super().info, msg, *args, **kwargs)

    def warning(self, msg: str, *args, **kwargs):
        self._pretty(super().warning, msg, *args, **kwargs)

    def error(self, msg: str, *args, **kwargs):
        self._pretty(super().error, msg, *args, **kwargs)

    def critical(self, msg: str, *args, **kwargs):
        self._pretty(super().critical, msg, *args, **kwargs)

    @staticmethod
    def _pretty(function, msg: str, *args, **kwargs):
        message = msg % args
        if "\n" not in message:
            function(message, **kwargs)
        else:
            parts = message.split("\n")
            for part in parts:
                function(part, **kwargs)

logging.setLoggerClass(PrettyLogger)
logger = logging.getLogger(__name__)


def get_length(value: str) -> int:
    length = 0
    for i in range(0, len(value)):
        print(i, value[i])
        length += 1
    return length


def ask(query: str) -> str:
    model = ChatOpenAI(temperature=0, api_key=os.environ["OPENAI_API_KEY"], max_tokens=4096)
    result = model.invoke([
        HumanMessage(content=query)
    ])
    return result.content

@dataclass(frozen=True)
class Step:
    content: str
    disable: bool = False


def create_nodes():
    @abstractmethod
    def _create_nodes():
        # create nodes in a flowchart include node's type and node's description
        pass

    nodes = _create_nodes()
    while len(nodes) != 20:
        nodes =  _create_nodes()
    return nodes

@dataclass(frozen=True)
class Steps:
    data: List[Step]

    @property
    def content(self):
        result = ""
        filter_data = [step for step in self.data if step.disable is False]
        for index, step in enumerate(filter_data):
            result += f"Step {index + 1}: {step.content}\n"

        return result

def main():
    steps: Steps = Steps([
        Step(
            content=f"This is a function definition {inspect.getsource(create_nodes)}."
                    # "Please create nodes with the function definition."
                    "Using chain of thought analysis steps to create nodes with the function definition."
                    "Output the result of each step."
        ),
        Step(
            content = "Create id for the created nodes.",
            disable = True
        ),
        Step(
            content = "Create edges to connect the nodes.",
            disable = True
        )
    ])
    logger.debug("Content %s", steps.content)

    query = f"""
    Provide results for all 3 steps.
    {steps.content}
    """
    logger.debug(query)
    result = ask(query=query)
    logger.info("Result %s", result)


if __name__ == "__main__":
    main()
