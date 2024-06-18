from abc import ABC, abstractmethod
from typing import Any


class Cache(ABC):
    @abstractmethod
    def key(self, value: Any) -> bytes:
        raise NotImplementedError()
