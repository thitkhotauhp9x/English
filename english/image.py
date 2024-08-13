from dataclasses import dataclass
from PIL import Image
from PIL.Image import Image as PilImage


@dataclass
class Image:
    image: PilImage

    @classmethod
    def open(cls, path: str) -> "Image":
        return cls(Image.open(path))
