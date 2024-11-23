from dataclasses import dataclass
from pathlib import Path
from typing import List
from tempfile import NamedTemporaryFile
from english.utils.executor import Executor


@dataclass
class OcrProcessor:
    path: Path
    languages: List[str]

    def ocr(self) -> bytes | None:
        with NamedTemporaryFile(suffix=".box") as temp_file:
            temp_path = Path(temp_file.name)

            executor = Executor(
                args=[
                    "tesseract",
                    self.path.as_posix(),
                    Path(temp_path.parent / temp_path.stem).as_posix(),
                    "-l",
                    "+".join(self.languages),
                    "batch.nochop",
                    "makebox",
                ]
            )
            executor.execute()
            return temp_path.read_bytes()
