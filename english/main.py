from english.utilities import OxfordLearnerDictionaries, RhymeZone
from english.wrappers import logging

logger = logging.getLogger(__name__)


def main():
    for word in RhymeZone(word="ham").words():
        phonetic = OxfordLearnerDictionaries(word=word).phonetic_br()
        if phonetic:
            logger.info("%s, %s", word, phonetic)


if __name__ == "__main__":
    main()
