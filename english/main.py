from pathlib import Path
from typing import List

from fastapi import FastAPI, UploadFile
from dataclasses import dataclass
from english.image import Image

app = FastAPI()


@app.post("/api/ocr")
def ocr(upload_file: UploadFile):
    file_name = upload_file.filename
    # files -> images
    suffix = Path(upload_file.filename).suffix.lower()

    if suffix in [".pdf"]:
        ...
    elif suffix in [".tif", ".tiff"]:
        ...
    else:
        ...

    print(upload_file.filename)


@dataclass
class Image: ...


@dataclass
class File:
    file_path: str

    def page_image(self, index: int) -> Image: ...
    def page_images(self) -> List[Image]: ...

    def page_number(self) -> int: ...


class PdfFile(File): ...
