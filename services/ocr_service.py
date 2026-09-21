import io
import cv2
import numpy as np
from PIL import Image

def preprocess_image(file_storage):
    data = file_storage.read()
    image = Image.open(io.BytesIO(data)).convert("RGB")
    arr = np.array(image)
    gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    _, threshold = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )
    return threshold

def extract_text(processed_image):
    try:
        import pytesseract
        text = pytesseract.image_to_string(processed_image, config="--psm 6")
        return " ".join(text.split())
    except Exception as exc:
        return (
            "OCR is not available. Install Tesseract OCR and make sure "
            "pytesseract can find tesseract.exe."
        )
