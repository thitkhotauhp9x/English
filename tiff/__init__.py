from tifffile import TiffFile
from dataclasses import dataclass
from typing import List


@dataclass
class ImagePage: ...


@dataclass
class Image:
    pages: List[ImagePage]
    ...


with TiffFile("001.tif") as tif:
    for page in tif.pages:
        image = page.asarray()
        print(image, type(image))
