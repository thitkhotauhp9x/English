from dataclasses import dataclass

from english.wrappers.cache.key_makers._base_key_maker import BaseKeyMaker


@dataclass
class DictKeyMaker(BaseKeyMaker):
    data: dict
    mark: tuple = (object(), "dict")

    def make(self) -> tuple:
        key = self.mark
        for item in self.data.items():
            key += item
        return key
