from dataclasses import dataclass
from ocr.box import Box


@dataclass
class Element:
    box: Box
    text: str
    #: Thành phần chứa thành phần khác hay không, index càng cao thì cảng ở lớp trên index càng nhỏ
    #: càng ở lớp dưới.
    index: int
