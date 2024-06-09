from dataclasses import dataclass


@dataclass
class BaseResult:
    stdout: bytes | None = None
    stderr: bytes | None = None
    return_code: int | None = None
