import re


def count_syllables(phonetic: str) -> int:
    pattern = "(eɪ|əʊ|aɪ|ɔɪ|aʊ|ɪə|eə|ʊə|iː|ɑː|uː|ɔː|ɜː|i|ɪ|ʌ|æ|ʊ|u|ɒ|e|ə)"
    return len(re.compile(pattern).findall(phonetic))


def find_vowel(phonetic: str) -> str:
    pattern = "(eɪ|əʊ|aɪ|ɔɪ|aʊ|ɪə|eə|ʊə|iː|ɑː|uː|ɔː|ɜː|i|ɪ|ʌ|æ|ʊ|u|ɒ|e|ə)"
    return ",".join(re.compile(pattern).findall(phonetic))
