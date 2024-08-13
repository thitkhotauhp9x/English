from itertools import groupby
from typing import Generator, Tuple, List
import logging
from tqdm import tqdm

from english.utilities import (
    RegexDict,
    OxfordLearnerDictionaries,
    find_vowel,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG,
)

logger = logging.getLogger(__name__)


def get_words(regex: str) -> Generator[Tuple[str, str], None, None]:
    for word_ in tqdm(list(RegexDict(regex).find())):
        phonetic = OxfordLearnerDictionaries(word_).phonetic_br()
        if phonetic is None:
            logger.debug("Cannot get the phonetic of the word=%r", word_)
            continue
        yield word_, phonetic


def make_report(regex: str) -> str:
    data: List[Tuple[str, str]] = list(get_words(regex))

    def _find_vowel(t: Tuple[str, str]) -> str:
        return find_vowel(t[1])

    content = f"{regex}\n"
    content += "===\n"
    for key, group in groupby(sorted(data, key=_find_vowel), key=_find_vowel):
        group_: list = list(group)
        percent = round(len(group_) * 100 / len(data))
        content += f"## {key} ({percent}%)\n"
        for w, p in group_:
            content += f"{w} {p}, "
        content += "\n"

    return content


def main():
    with open("output.md", "a") as output:
        content = make_report(regex="^[^ueoaiy-]*o[^ueoaiyr]{2}e[^-wueoraiy]*$")
        print(content)
        output.write(content)


if __name__ == "__main__":
    main()
