from dataclasses import dataclass
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import List

from ocr.popen_executor import PopenExecutor


@dataclass
class OcrProcessor:
    path: Path
    languages: List[str]

    def ocr(self) -> bytes | None:
        with NamedTemporaryFile(suffix=".box") as temp_file:
            temp_path = Path(temp_file.name)

            PopenExecutor(
                args=[
                    "tesseract",
                    self.path.as_posix(),
                    Path(temp_path.parent / temp_path.stem).as_posix(),
                    "-l",
                    "+".join(self.languages),
                    "batch.nochop",
                    "makebox",
                ]
            ).execute()
            return temp_path.read_bytes()

    @staticmethod
    def list_langs():
        PopenExecutor(args=["tesseract", "--list-langs"]).execute()
