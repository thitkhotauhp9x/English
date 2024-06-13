from abc import ABC
from shlex import quote, join
from subprocess import Popen, PIPE
from typing import List

from english.wrappers.execute._result import BaseResult


class BaseExecutor(ABC):
    @property
    def command(self) -> str:
        return join([quote(arg) for arg in self.args])

    @property
    def args(self) -> List[str]:
        raise NotImplementedError()

    def execute(self, timeout: int | None = None) -> BaseResult:
        with Popen(self.command, stdout=PIPE, stderr=PIPE) as proc:
            stdout, stderr = proc.communicate(timeout=timeout)

            return BaseResult(
                stdout=stdout,
                stderr=stderr,
                return_code=proc.returncode,
            )
