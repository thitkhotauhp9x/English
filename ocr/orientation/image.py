from dataclasses import dataclass
from typing import Generator, Self

from PIL import Image as Img
from PIL.Image import Image as TypeImg
from contextlib import contextmanager


@dataclass
class Image:
    image: TypeImg

    def rotate(self, angle: float) -> Self:
        self.image = self.image.rotate(angle, expand=True, fillcolor="white")
        return self

    def deskew(self, angle: float) -> Self:
        self.image = self.image.rotate(angle, expand=False, fillcolor="white")
        return self

    def show(self) -> None:
        return self.image.show()

    def save(self, file: str) -> None:
        self.image.save(file)

    def ocr(self, languages: str) -> str: ...

    def detect_lang(self): ...

    @classmethod
    @contextmanager
    def open(cls, file: str) -> Generator["Image", None, None]:
        with Img.open(file) as image:
            yield cls(image)
