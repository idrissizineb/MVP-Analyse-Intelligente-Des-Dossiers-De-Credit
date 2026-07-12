import cv2

from app.ocr.paddle_ocr import PaddleOCRProcessor

print("TEST STARTED")

IMAGE_PATH = "data/processed/page_1_resized.png"

image = cv2.imread(IMAGE_PATH)

if image is None:
    raise FileNotFoundError(f"Could not load image: {IMAGE_PATH}")

print("Image loaded successfully")

ocr = PaddleOCRProcessor()

print("OCR initialized")

results = ocr.recognize(image)

print("OCR finished")

print(results)