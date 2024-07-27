from PIL import Image
import pytesseract
from langdetect import detect


def rotate_image(image_path, angle):
    """Xoay ảnh theo góc cho trước.

    Args:
        image_path (str): Đường dẫn đến ảnh.
        angle (int): Góc xoay (tính theo độ).

    Returns:
        PIL.Image: Ảnh đã xoay.
    """
    image = Image.open(image_path)
    rotated_image = image.rotate(angle)
    return rotated_image


def extract_text_from_image(image):
    """Thực hiện OCR trên ảnh và trả về văn bản.

    Args:
        image (PIL.Image): Ảnh để trích xuất văn bản.

    Returns:
        str: Văn bản trích xuất từ ảnh.
    """
    text = pytesseract.image_to_string(image)
    return text


def detect_language(text):
    """Xác định ngôn ngữ của văn bản.

    Args:
        text (str): Văn bản để xác định ngôn ngữ.

    Returns:
        str: Ngôn ngữ được xác định.
    """
    try:
        language = detect(text)
        return language
    except:
        return "Không thể xác định ngôn ngữ."


# Ví dụ sử dụng
image_path = "image.jpg"  # Thay đổi đường dẫn đến ảnh của bạn
angles = [90, 180, 270]  # Các góc xoay

for angle in angles:
    rotated_image = rotate_image(image_path, angle)
    # Thực hiện OCR trên ảnh đã xoay
    text = extract_text_from_image(rotated_image)
    print(f"Text from rotated image ({angle} degrees):\n{text}")
    # Xác định ngôn ngữ của văn bản
    language = detect_language(text)
    print(f"Ngôn ngữ của văn bản: {language}")
    rotated_image.save(f"rotated_{angle}.jpg")
