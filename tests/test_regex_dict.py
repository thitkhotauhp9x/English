from unittest import TestCase
from english.utilities import RegexDict


class TestRegexDict(TestCase):

    def test_sequence(self):
        words = RegexDict(regex=".*", ps="x", fstr="").find()
        for word in words:
            print(word)
