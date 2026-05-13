import shelve
from collections import UserList
from dataclasses import dataclass


@dataclass
class Word:
    word: str
    phonetic: str


class WordList(UserList[Word]):

    def find_phonetic(self, word: str) -> str | None:
        for item in self.data:
            if item.word == word:
                return item.phonetic
        return None
