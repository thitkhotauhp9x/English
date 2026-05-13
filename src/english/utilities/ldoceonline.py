import pickle
import shelve

from bs4 import BeautifulSoup
from requests import get


class Longman:
    @staticmethod
    def get_page(word: str):
        with shelve.open("longman.db") as db:
            if word not in db:
                url = f"https://www.ldoceonline.com/dictionary/{word}"
                response = get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
                soup = BeautifulSoup(response.text, "html.parser")
                db[word] = pickle.dumps(soup)
            return pickle.loads(db[word])

    @staticmethod
    def get_hyphenation(word: str):
        soup = Longman.get_page(word)
        hyphenation = soup.find("span", class_="HYPHENATION")
        if hyphenation:
            text = hyphenation.text
            return text.split("‧")
        return None

    @staticmethod
    def get_phonetic(word: str):
        soup = Longman.get_page(word)
        pron_codes = soup.find("span", class_="PronCodes")
        if pron_codes:
            phonetic = pron_codes.find("span", class_="PRON")
            if phonetic:
                return phonetic.text
        return None


def main():
    hyphen = Longman.get_hyphenation("ridicule")
    phonetic = Longman.get_phonetic("ridicule")
    print(hyphen)
    print(phonetic)
    # r -> r
    # i -> I (1), i -> @ (2), i-> None (3)
    # d -> d (4),
    # i -> @
    # c -> k
    # u -> ju:
    # l -> l
    # e -> None


if __name__ == "__main__":
    main()
