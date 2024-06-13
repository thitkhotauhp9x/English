from dataclasses import dataclass
from pathlib import Path


@dataclass
class CachedPath:
    path: Path

    def __hash__(self):
        return hash(self.path.read_bytes())
