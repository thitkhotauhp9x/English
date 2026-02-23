from enum import StrEnum


class PhoneticTag(StrEnum):
    UNKNOWN = "unknown"
    CONSONANT = "consonant"
    VOWEL = "vowel"
    STRESS = "stress"
