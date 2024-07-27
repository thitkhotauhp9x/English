from dataclasses import dataclass
from ocr.pixel import Px


@dataclass
class Box:
    x: Px
    y: Px
    width: Px
    height: Px
