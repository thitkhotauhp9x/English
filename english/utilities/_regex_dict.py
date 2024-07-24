import re
from abc import ABC
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Mapping, Any, Generator, Literal

from bs4 import BeautifulSoup
from requests import post, Response


@lru_cache(maxsize=None)
def get_words(url: str, regex: str) -> Response:
    data = {
        "str": regex,
        "ifun": "if",
        "ccg": "all",
        "search": "Search",
    }
    response = post(url=url, data=data, timeout=None, headers={"User-Agent": "Mozilla/5.0"})
    return response


@dataclass
class RegexDict(ABC):
    regex: str
    url: str = field(default="https://www.visca.com/regexdict/")
    headers: Mapping[Any, Any] = field(default_factory=lambda: {"User-Agent": "Mozilla/5.0"})
    timeout: int | None = field(default=None)
    ifun: str = field(default="if")
    ccg: str = field(default="all")
    search: str = field(default="Search")
    fstr: str | None = field(default=None)
    ps: Literal["x"] | None = field(default=None)

    @property
    def data(self) -> Mapping[Any, Any]:
        result = {
            "str": self.regex,
            "ifun": self.ifun,
            "ccg": self.ccg,
            "search": self.search,
        }

        if self.fstr is not None:
            result["fstr"] = self.fstr
        if self.ps is not None:
            result["ps"] = self.ps

        return result

    def request(self) -> Response:
        return post(url=self.url, data=self.data, timeout=None, headers={"User-Agent": "Mozilla/5.0"})

    def find(self) -> Generator[str, None, None]:
        response = self.request()
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            for a in soup.find_all("a"):
                text = a.text
                result = re.compile(r"^-?\w+-?$").match(text)
                if result is not None:
                    yield text
