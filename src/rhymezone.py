from dataclasses import dataclass
from requests import get
from bs4 import BeautifulSoup


@dataclass
class RhymeZone:
    word: str

    def words(self):
        url = f"https://www.rhymezone.com/r/rhyme.cgi?Word={self.word}&typeofrhyme=cons&org1=syl@org2=l&org3=y"
        response = get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "html.parser")
        for r in soup.find_all("a", class_="r"):
            yield r.text
