from dataclasses import dataclass
from subprocess import Popen, PIPE
from typing import List

from ocr.base_executor import BaseExecutor


@dataclass
class PopenExecutor(BaseExecutor):
    args: List[str]

    def execute(self):
        with Popen(self.args, stdin=PIPE, stdout=PIPE) as p:
            stdout, stderr = p.communicate()
            print(stdout, stderr)
