from typing import Generator, NamedTuple

from utilities._phonetic import Phonetic
from utilities._phonetic_tag import PhoneticTag


class Word(NamedTuple):
    word: str
    phonetic: str

    def groups(self):
        phonetic = Phonetic(phonetic=self.phonetic)
        return phonetic.groups()

    def vowels(self) -> Generator[str, None, None]:
        phonetic = Phonetic(phonetic=self.phonetic)
        for key, value in phonetic.groups():
            if key == PhoneticTag.VOWEL:
                yield value
