import pickle
from collections import UserList
<<<<<<< HEAD
from functools import lru_cache
=======
>>>>>>> d9bfdc1 (...)
from itertools import groupby
from pathlib import Path
from typing import Generator, Tuple, List
from typing import NamedTuple

from tqdm import tqdm

# from english.reporter import create_note
from english.utilities import RegexDict, OxfordLearnerDictionaries, count_syllables, find_vowel
from english.wrappers.cache import memoize


class Word(NamedTuple):
    word: str
    phonetic: str


class WordList(UserList):
    ...


@memoize()
def get_words(word: str) -> WordList:
    word_list: WordList = WordList()
    for word_ in tqdm(list(RegexDict(word).find())):
        phonetic = OxfordLearnerDictionaries(word_).phonetic_br()
        word_list.append(Word(word=word_, phonetic=phonetic))
    return word_list


@memoize()
def get_filter_words(word: str, num: int) -> WordList:
    mono_list = WordList()
    word_list = get_words(word)
    for word_, phonetic in word_list:
        if phonetic is None:
            continue
        total = count_syllables(phonetic)
        if total == num:
            mono_list.append(Word(word_, phonetic))
    return mono_list


class Word(NamedTuple):
    word: str
    phonetic: str


class WordList(UserList):
    ...


@lru_cache(maxsize=None)
def get_words(word: str) -> WordList:
    word_list: WordList = WordList()
    for word in tqdm(list(RegexDict(word).find())):
        phonetic = OxfordLearnerDictionaries(word).phonetic_br()
        word_list.append(Word(word=word, phonetic=phonetic))
    return word_list


@lru_cache(maxsize=None)
def get_filter_words(word: str, num: int) -> WordList:
    mono_list = WordList()
    word_list = get_words(word)
    for word, phonetic in word_list:
        if phonetic is None:
            continue
        total = count_syllables(phonetic)
        if total == num:
            mono_list.append(Word(word, phonetic))
    return mono_list


def filter_(word: str, num: int) -> Generator[Tuple[str, str], None, None]:
    path = Path(f"{word}.pickle")
    if not path.exists():
        data = []
        for word_ in tqdm(list(RegexDict(word).find())):
            phonetic = OxfordLearnerDictionaries(word_).phonetic_br()
            data.append((word_, phonetic))

        with open(path.as_posix(), "wb") as f:
            pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

    with open(path.as_posix(), "rb") as f:
        for word_, phonetic in pickle.load(f):
            if phonetic is None:
                continue
            total = count_syllables(phonetic)
            if total == num:
                yield word_, phonetic
            else:
                ...


def make_report(word: str) -> None:
    data: List[Tuple[str, str]] = list(filter_(word, 1))

    def _find_vowel(t: Tuple[str, str]) -> str:
        return find_vowel(t[1])

    content = f"{word}\n"
    content += "===\n"
    for key, group in groupby(sorted(data, key=_find_vowel), key=_find_vowel):
        group_: list = list(group)
        percent = round(len(group_) * 100 / len(data))
        content += f"## {key} ({percent}%)\n"
        for w, p in group_:
            content += f"{w} {p}, "
        content += "\n"

    # create_note(title=f"{word}", content=content)


def make_report_v2(word: str) -> List[tuple]:
    data: WordList = get_filter_words(word, 1)

    def _find_vowel(t: Tuple[str, str]) -> str:
        return find_vowel(t[1])

    ana_data = []
    for key, group in groupby(sorted(data, key=_find_vowel), key=_find_vowel):
        group = list(group)
        percent = round(len(group) * 100 / len(data))
        ana_data.append((key, percent, group))

    def _filter(item):
        _, p, _ = item
        return p

    sorted(ana_data, key=_filter)
    return ana_data


def main():
    make_report(word="ie[^rueoai]e")


if __name__ == "__main__":
    main()
