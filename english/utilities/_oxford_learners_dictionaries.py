from dataclasses import dataclass
from typing import Optional

from bs4 import BeautifulSoup
from requests import get, Response
from english.wrappers.cache import memoize


@memoize()
def get_definition(word: str, timeout: int | None) -> Response:
    url = f"https://www.oxfordlearnersdictionaries.com/definition/english/{word}"
    response = get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=timeout)
    return response


@dataclass
class OxfordLearnerDictionaries:
    word: str

    def phonetic_br(self, timeout: Optional[int] = None):
        response = get_definition(self.word, timeout)
        soup = BeautifulSoup(response.text, "html.parser")

        container = soup.find("div", class_="top-container")
        if container is None:
            return None
        phones_br = container.find("div", class_="phons_br")  # type: ignore
        if phones_br is None:
            return None
        phon = phones_br.find("span", class_="phon")  # type: ignore
        if phon is None:
            return None
        return phon.text  # type: ignore
