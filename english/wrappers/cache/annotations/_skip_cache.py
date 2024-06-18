import pickle
from dataclasses import dataclass
from typing import Any

from english.wrappers.cache.annotations._cache import Cache


@dataclass
class SkipCache(Cache):
    def key(self, value: Any) -> bytes:
        return pickle.dumps((object(), "skip"))
