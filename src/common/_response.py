from dataclasses import dataclass

from requests import Response as _Response


@dataclass(frozen=True)
class Response:
    response: _Response
