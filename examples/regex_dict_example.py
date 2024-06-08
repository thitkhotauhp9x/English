import pickle
from pathlib import Path
from typing import Generator, Tuple

from tqdm import tqdm

from english.utilities import RegexDict, OxfordLearnerDictionaries, count_syllables


def filter_(word: str, num: int) -> Generator[Tuple[str, str], None, None]:
    path = Path("data.pickle")
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


def main():
    for word, phonetic in filter_("ear", 1):
        print(word, phonetic)


if __name__ == "__main__":
    main()
