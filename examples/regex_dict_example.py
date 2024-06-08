import pickle
from pathlib import Path

from tqdm import tqdm

from english.utilities import RegexDict, OxfordLearnerDictionaries


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
            print(word, phonetic)


if __name__ == "__main__":
    main()
