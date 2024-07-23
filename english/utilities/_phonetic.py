from dataclasses import dataclass
from typing import List

import regex as re


@dataclass
class Phonetic:
    phonetic: str

    @staticmethod
    def get_pattern(regex):
        pattern = rf"""
        (?(DEFINE)
            (?<long_vowel>iː|ɑː|uː|ɔː|ɜː)
            (?<short_vowel>i|ɪ|ʌ|æ|ʊ|u|ɒ|e|ə)
            (?<diphthong>eɪ|əʊ|aɪ|ɔɪ|aʊ|ɪə|eə|ʊə)
            (?<consonant>tʃ|dʒ|p|b|t|d|k|g|f|v|θ|ð|s|z|ʃ|ʒ|h|m|n|ŋ|l|r|j|w)
            (?<vowel>(?&diphthong)|(?&long_vowel)|(?&short_vowel))
            (?<phonetic>(?&vowel)|(?&consonant))
            (?<stress>ˈ)
        )
        {regex}
        """
        return re.sub(r"\s", "", pattern)

    def vowels(self) -> List[str]:
        pattern = self.get_pattern("(?&vowel)|(?&stress)")
        return list(re.compile(pattern).findall(self.phonetic))

    def parts(self) -> List[str]:
        pattern = self.get_pattern("(?&phonetic)")
        formated_pattern = re.sub(r"\s", "", pattern)
        return list(re.compile(formated_pattern).findall(self.phonetic))
