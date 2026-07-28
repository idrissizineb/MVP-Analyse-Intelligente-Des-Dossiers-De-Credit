from pathlib import Path

from app.pipeline import DocumentPipeline


def main():

    input_folder = Path("data/input")

    pdf_files = sorted(input_folder.glob("*.pdf"))

    if not pdf_files:

        print("No PDF files found.")

        return

    print("=" * 60)
    print(f"{len(pdf_files)} PDF(s) found.")
    print("=" * 60)

    for pdf_file in pdf_files:

        print("\n" + "=" * 60)
        print(f"PROCESSING: {pdf_file.name}")
        print("=" * 60)

        pipeline = DocumentPipeline(
            pdf_path=str(pdf_file),
            save_intermediate=True
        )

        try:

            result = pipeline.run()

        except Exception as error:

            print(f"\n❌ Error while processing {pdf_file.name}")
            print(error)

            continue

        print("\n========== SUMMARY ==========\n")

        print(f"Document : {pdf_file.name}")

        print(f"Dossier ID : {result['dossier_id']}")

        print(f"Document ID : {result['document_id']}")

        print("\nExtracted Fields:\n")

        for field, value in result["fields"].items():

            print(f"{field}: {value}")

        print("\nValidation:")

        print(result["validation"]["is_valid"])

        print("\nFinished.")

    print("\n" + "=" * 60)
    print("ALL DOCUMENTS HAVE BEEN PROCESSED")
    print("=" * 60)


if __name__ == "__main__":

    main()