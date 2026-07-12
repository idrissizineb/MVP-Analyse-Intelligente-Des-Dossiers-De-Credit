from app.pipeline import DocumentPipeline


def main():

    pipeline = DocumentPipeline(
        pdf_path="data/input/-3.pdf",
        save_intermediate=True
    )

    processed_pages = pipeline.run()

    print(f"\nTotal processed pages: {len(processed_pages)}")


if __name__ == "__main__":
    main()