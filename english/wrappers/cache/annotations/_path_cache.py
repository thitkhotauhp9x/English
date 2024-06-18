from dataclasses import dataclass
from pathlib import Path

from english.wrappers.cache.annotations._cache import Cache
from english.wrappers.cache.errors import CacheError


@dataclass
class PathCache(Cache):
    path: Path

    def key(self, path: Path) -> bytes:
        if path.exists() and path.is_file():
            return path.read_bytes()
        raise CacheError(f"Cannot read the file {path}")
