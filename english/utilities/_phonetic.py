import itertools
from dataclasses import dataclass
from typing import List, Generator, Tuple

import regex as re

from english.utilities._phonetic_tag import PhoneticTag


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

    def groups(self) -> Generator[Tuple[PhoneticTag, str], None, None]:
        def _group_by(_phonetic_letter: chr) -> PhoneticTag:
            consonant_pattern = self.get_pattern("(?&consonant)")
            if re.match(consonant_pattern, _phonetic_letter):
                return PhoneticTag.CONSONANT

            vowel_pattern = self.get_pattern("(?&vowel)")
            if re.match(vowel_pattern, _phonetic_letter):
                return PhoneticTag.VOWEL

            stress_pattern = self.get_pattern("(?&stress)")
            if re.match(stress_pattern, _phonetic_letter):
                return PhoneticTag.STRESS

            return PhoneticTag.UNKNOWN

        for key, group in itertools.groupby(self.phonetic, key=_group_by):
            yield key, "".join(group)
