from app.postprocessing.ocr_postprocessor import OCRPostProcessor


ocr_results = [
    {
        "text": "Faculté des Sciences",
        "confidence": 0.95,
        "polygon": []
    },
    {
        "text": "55555",
        "confidence": 0.58,
        "polygon": []
    },
    {
        "text": "IDRISSI ZINEB",
        "confidence": 0.97,
        "polygon": []
    },
    {
        "text": "hlw1",
        "confidence": 0.60,
        "polygon": []
    }
]


processor = OCRPostProcessor(
    min_confidence=0.70
)

filtered = processor.filter_confidence(ocr_results)

print("\nRemaining OCR Results:\n")

for result in filtered:
    print(result)