#: pylint: disable=invalid-name

from abc import abstractmethod
from pathlib import Path
from typing import Optional
from unittest import TestCase

from PyPDF2 import PdfReader


class BaseTestCase(TestCase):
    def assertIsPdf(self, path: Path, page_number: Optional[int] = None, has_text: Optional[bool] = None) -> None:
        self.assertEqual(path.suffix.lower(), ".pdf")

        reader = PdfReader(path)

        if isinstance(page_number, int):
            self.assertEqual(reader.pages, page_number)

        if isinstance(has_text, bool):
            text = "".join([page.extract_text() for page in reader.pages])
            if has_text is True:
                self.assertNotEqual(text, "")
            else:
                self.assertEqual(text, "")

    @abstractmethod
    def assertIsTiff(self, path: Path, page_number: Optional[int] = None, has_text: Optional[bool] = None) -> None:
        ...
