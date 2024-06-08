import pickle
from pathlib import Path

from tqdm import tqdm

from english.utilities import RegexDict, OxfordLearnerDictionaries, count_syllables


def main():
    path = Path("data.pickle")
    if not path.exists():
        data = []
        for word in tqdm(list(RegexDict("ear").find())):
            phonetic = OxfordLearnerDictionaries(word).phonetic_br()
            data.append((word, phonetic))

        with open(path.as_posix(), "wb") as f:
            pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

    with open(path.as_posix(), "rb") as f:
        for word, phonetic in pickle.load(f):
            if phonetic is None:
                continue
            total = count_syllables(phonetic)
            if total == 1:
                print(word, phonetic)
            else:
                ...


if __name__ == "__main__":
    main()
