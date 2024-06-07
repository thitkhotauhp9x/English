from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List


@dataclass
class RegexDict(ABC):
    @abstractmethod
    def find(self, regex: str) -> List[str]:
        # response: Response = Requests().get(url="")
        ...
