import re
from pathlib import Path
from PIL import Image
from PIL import ImageDraw

from ocr.ocr_processor import OcrProcessor

if __name__ == "__main__":
    boxes = (
        OcrProcessor(path=Path("./001.png"), languages=["eng"]).ocr().decode("utf-8")
    )

    image = Image.open("./001.png")

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
