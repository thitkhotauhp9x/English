from dataclasses import dataclass, field
from typing import List, Tuple

from english.wrappers.cache.key_makers._base_key_maker import BaseKeyMaker


@dataclass
class KeyMaker(BaseKeyMaker):
    makers: List[BaseKeyMaker] = field(default_factory=lambda: [])

    def add_maker(self, maker: BaseKeyMaker) -> None:
        self.makers.append(maker)

    def make(self) -> tuple:
        key: Tuple = tuple()
        for maker in self.makers:
            key += maker.make()
        return key
