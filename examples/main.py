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
        regex="^[^ueoaiy-]*o[^ueoaiyr]{2}e[^-wueoraiy]*$"
    )
    content = phonetic_analysis.make_report()
    print(content)


if __name__ == "__main__":
    main()
