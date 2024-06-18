from dataclasses import dataclass

from english.wrappers.cache.key_makers._base_key_maker import BaseKeyMaker


@dataclass
class TupleKeyMaker(BaseKeyMaker):
    data: tuple

    def make(self) -> tuple:
        return self.data
