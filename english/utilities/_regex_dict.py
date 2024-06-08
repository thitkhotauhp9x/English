import re
from abc import ABC
from dataclasses import dataclass, field
from typing import Mapping, Any, Generator

from bs4 import BeautifulSoup
from requests import post


@dataclass
class RegexDict(ABC):
    regex: str
    url: str = field(default="https://www.visca.com/regexdict/")
    headers: Mapping[Any, Any] = field(default_factory=lambda: {"User-Agent": "Mozilla/5.0"})
    timeout: int | None = field(default=None)

    @property
    def data(self) -> Mapping[Any, Any]:
        return {
            "str": self.regex,
            "ifun": "if",
            "ccg": "all",
            "search": "Search",
        }

    def find(self) -> Generator[str, None, None]:
        response = post(url=self.url, data=self.data, timeout=self.timeout, headers=self.headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            for a in soup.find_all("a"):
                text = a.text
                result = re.compile(r"^\w+$").match(text)
                if result is not None:
                    yield text
