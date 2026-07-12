from paddleocr import PaddleOCR

ocr = PaddleOCR(
    lang="fr",
    use_doc_orientation_classify=True,
    use_textline_orientation=True,
)

results = ocr.predict("data/processed/page_1_resized.png")

print(results)