import logging
from dataclasses import dataclass
from itertools import groupby
from typing import Generator, List

from tqdm import tqdm

from english.utilities._common import find_vowel
from english.utilities._oxford_learners_dictionaries import OxfordLearnerDictionaries
from english.utilities._regex_dict import RegexDict
from english.utilities._word import Word

logger = logging.getLogger(__name__)


@dataclass
class PhoneticAnalysis:
    regex: str

    def get_words(self) -> Generator[Word, None, None]:
        for word_ in tqdm(list(RegexDict(self.regex).find())):
            phonetic = OxfordLearnerDictionaries(word_).phonetic_br()
            if phonetic is None:
                logger.debug("Cannot get the phonetic of the word=%r", word_)
                continue
            yield Word(word=word_, phonetic=phonetic)

    def make_report(self) -> str:
        data: List[Word] = list(self.get_words())

        data = [word for word in data if len(list(word.vowels())) == 1]

        def _find_vowel(t: Word) -> str:
            return find_vowel(t[1])

        content = f"{self.regex}\n"
        content += "===\n"

        for key, group in groupby(sorted(data, key=_find_vowel), key=_find_vowel):
            group_: list = list(group)
            percent = round(len(group_) * 100 / len(data))
            content += f"## {key} ({percent}%)\n"
            for w, p in group_:
                content += f"{w} {p}, "
            content += "\n"

        return content
