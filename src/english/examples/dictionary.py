
import json
from collections import UserDict
from typing import Dict, Any, Union

class Dictionary(UserDict):

    def to_compact_json_string(self) -> str:
        return json.dumps(self.data, separators=(',', ':'))

    def delete_items_recursive(self, key: str) -> None:
        self._delete_items_recursive(self.data, key)

    @staticmethod
    def _delete_items_recursive(items: Union[Dict[str, Any], list], key: str) -> None:
        if isinstance(items, dict):
            if key in items:
                del items[key]
            for k, v in items.items():
                Dictionary._delete_items_recursive(v, key)
        elif isinstance(items, list):
            for item in items:
                Dictionary._delete_items_recursive(item, key)
