import pickle
from itertools import groupby
from pathlib import Path
from typing import Generator, Tuple, List

from tqdm import tqdm

from english.utilities import RegexDict, OxfordLearnerDictionaries, count_syllables, find_vowel


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

    with open(f"{word}.md", "w", encoding="utf-8") as writer:
        for key, group in groupby(sorted(data, key=_find_vowel), key=_find_vowel):
            writer.write(f"## {key}\n")
            for w, p in group:
                writer.write(f"* {w} {p}\n")


def main():
    make_report(word="ee")


if __name__ == "__main__":
    main()
