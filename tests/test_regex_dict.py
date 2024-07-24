from unittest import TestCase
from english.utilities import RegexDict


def get_suffixes():
    return RegexDict(regex="-.*", ps="x", fstr="").find()


class TestRegexDict(TestCase):

    def test_suffixes(self):
        suffixes = list(get_suffixes())
        self.assertEqual(len(suffixes), 336)
