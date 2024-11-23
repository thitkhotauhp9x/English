import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from subprocess import Popen, PIPE
from typing import List

logger = logging.getLogger(__name__)


@dataclass
class BaseResult:
    stdout: bytes
    stderr: bytes


class BaseExecutor(ABC):
    @abstractmethod
    def execute(self) -> BaseResult:
        pass


@dataclass
class Executor(BaseExecutor):
    args: List[str]

    def execute(self) -> BaseResult:
        with Popen(self.args, stdin=PIPE, stdout=PIPE) as p:
            stdout, stderr = p.communicate()
            return BaseResult(stdout, stderr)
