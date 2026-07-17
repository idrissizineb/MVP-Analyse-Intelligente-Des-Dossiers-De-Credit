from app.pipeline import DocumentPipeline


def main():

    pipeline = DocumentPipeline(
        pdf_path="data/input/FICHE DE DECISION TEST.pdf",
        save_intermediate=True
    )

    processed_pages = pipeline.run()

    print(f"\nTotal processed pages: {len(processed_pages)}")
    print("\n========== OCR RESULTS ==========\n")

    for page in processed_pages:
        for line in page["ocr"]:
            print(line)


if __name__ == "__main__":
    main()