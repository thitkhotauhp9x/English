from dataclasses import dataclass
from requests import get
from bs4 import BeautifulSoup


@dataclass
class OxfordLearnerDictionaries:
    word: str

    @property
    def phonetic_br(self):
        url = f"https://www.oxfordlearnersdictionaries.com/definition/english/{self.word}"
        response = get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "html.parser")

        container = soup.find("div", class_="top-container")
        if container is None:
            return None
        phones_br = container.find("div", class_="phons_br")
        if phones_br is None:
            return None
        phon = phones_br.find("span", class_="phon")
        if phon is None:
            return None
        return phon.text
