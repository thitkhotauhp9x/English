import inspect
from dataclasses import dataclass
from typing import Callable

from english.wrappers.cache.key_makers._base_key_maker import BaseKeyMaker


@dataclass
class FuncKeyMaker(BaseKeyMaker):
    data: Callable
    mark: tuple = (object(), "func")

    def make(self) -> tuple:
        key = self.mark
        key += (inspect.getsource(self.data),)
        return key
