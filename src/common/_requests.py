from dataclasses import dataclass
from functools import cached_property
from typing import Optional

from requests import get

from ._response import Response
from ._types import Headers


@dataclass(frozen=True)
class Requests:
    @cached_property
    def headers(self) -> Headers:
        return {
            "User-Agent": "Mozilla/5.0",
        }

    def get(self, url: str, timeout: Optional[int] = None) -> Response:
        return Response(get(url, headers=self.headers, timeout=timeout))
