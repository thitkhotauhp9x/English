from dataclasses import dataclass

from bs4 import BeautifulSoup
from requests import get


@dataclass
class UrbanDictionary:
    word: str

    def content(self):
        url = f"https://www.urbandictionary.com/define.php?term={self.word}"
        response = get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=60)
        soup = BeautifulSoup(response.text, "html.parser")
        print(soup)


def main():
    UrbanDictionary("bluff").content()


if __name__ == "__main__":
    main()
