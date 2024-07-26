import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List
from subprocess import Popen, PIPE
from abc import ABC, abstractmethod
from tempfile import NamedTemporaryFile
from PIL import Image
from PIL import ImageDraw


class BaseExecutor(ABC):
    @abstractmethod
    def execute(self): ...


@dataclass
class PopenExecutor(BaseExecutor):
    args: List[str]

    def execute(self):
        with Popen(self.args, stdin=PIPE, stdout=PIPE) as p:
            stdout, stderr = p.communicate()
            # print(stdout, stderr)


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


if __name__ == "__main__":
    boxes = (
        OcrProcessor(path=Path("./001.png"), languages=["eng"]).ocr().decode("utf-8")
    )

    image = Image.open("./001.png")
    # image
    HEIGHT = image.height
    draw = ImageDraw.Draw(image)

    for box in re.compile(r"(.*) (\d+) (\d+) (\d+) (\d+) (\d+)\n").findall(boxes):
        text, left, bottom, right, top, page_number = box

        left = int(left)
        bottom = int(bottom)
        right = int(right)
        top = int(top)

        left_top_point = (left, HEIGHT - top)
        right_bottom_point = (right, HEIGHT - bottom)
        print(left_top_point, right_bottom_point)
        draw.rectangle((left_top_point, right_bottom_point), width=1)

    image.show()
