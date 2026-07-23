from app.pipeline import DocumentPipeline


def main():

    pipeline = DocumentPipeline(
        pdf_path="data/input/FICHE DE DECISION TEST.pdf",
        save_intermediate=True
    )

    result = pipeline.run()

    processed_pages = result["pages"]
    extracted_fields = result["fields"]

    print(f"\nTotal processed pages: {len(processed_pages)}")

    print("\n========== EXTRACTED FIELDS ==========\n")

    for field, value in extracted_fields.items():
        print(f"{field}: {value}")

    print("\n========== OCR RESULTS ==========\n")

    for page_number, page in enumerate(
        processed_pages,
        start=1
    ):

        print(f"\n===== PAGE {page_number} =====\n")
        print(page["corrected_text"])


if __name__ == "__main__":
    main()