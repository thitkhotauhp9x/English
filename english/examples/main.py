import logging

from english.utilities import PhoneticAnalysis

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG,
)

logger = logging.getLogger(__name__)


def main():
    phonetic_analysis = PhoneticAnalysis(
        regex="^[^ueoai]*[a]+[^ueorai]*$"
    )
    words = phonetic_analysis.get_words()
    words = [word for word in words if len(list(word.vowels())) == 1]
    for word in words:
        print(word.word)


if __name__ == "__main__":
    main()
