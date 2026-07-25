from pathlib import Path
import cv2
import json

from app.preprocessing.loader import DocumentLoader
from app.preprocessing.pdf_converter import PDFConverter
from app.preprocessing.grayscale import GrayscaleConverter
from app.preprocessing.deskew import DeskewCorrector
from app.preprocessing.denoise import Denoiser
from app.preprocessing.contrast import ContrastEnhancer
from app.preprocessing.resize import ImageResizer

from app.ocr.paddle_ocr import PaddleOCRProcessor

from app.postprocessing.ocr_postprocessor import OCRPostProcessor
from app.postprocessing.text_reconstructor import TextReconstructor

from app.llm.groq_client import GroqClient
from app.llm.field_extractor import FieldExtractor

from app.validation.validator import Validator

from app.normalization.normalizer import Normalizer
from data.database.connection import DatabaseConnection  # pyright: ignore[reportMissingImports]
from data.database.database_manager import DatabaseManager  # pyright: ignore[reportMissingImports]


class DocumentPipeline:
    """
    End-to-end Intelligent Document Processing pipeline
    for banking documents.

    Pipeline:
        1. Validate the input document
        2. Convert the PDF into page images
        3. Convert images to grayscale
        4. Correct document skew
        5. Remove image noise
        6. Enhance image contrast
        7. Resize images for OCR
        8. Perform OCR using PaddleOCR
        9. Filter low-confidence OCR detections
        10. Sort OCR results according to reading order
        11. Reconstruct OCR detections into readable text
        12. Correct OCR errors using the LLM
        13. Extract structured banking fields
        14. Validate the extracted fields
        15. Return the complete processing results
    """

    def __init__(
        self,
        pdf_path: str,
        output_dir: str = "data/processed",
        save_intermediate: bool = True,
    ):
        """
        Initialize the document processing pipeline.

        Parameters
        ----------
        pdf_path : str
            Path to the input PDF document.

        output_dir : str
            Directory used to save intermediate results.

        save_intermediate : bool
            Whether to save intermediate images and OCR results.
        """

        # ==========================================================
        # Configuration
        # ==========================================================

        self.pdf_path = pdf_path
        self.output_dir = Path(output_dir)
        self.save_intermediate = save_intermediate

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        # ==========================================================
        # Document loading and PDF conversion
        # ==========================================================

        self.loader = DocumentLoader(
            self.pdf_path
        )

        self.converter = PDFConverter(
            self.pdf_path
        )

        # ==========================================================
        # Image preprocessing
        # ==========================================================

        self.grayscale = GrayscaleConverter()

        self.deskew = DeskewCorrector()

        self.denoiser = Denoiser(
            method="nlm"
        )

        self.contrast = ContrastEnhancer()

        self.resizer = ImageResizer(
            target_longest_side=2500
        )

        # ==========================================================
        # OCR
        # ==========================================================

        self.ocr = PaddleOCRProcessor()

        # ==========================================================
        # OCR post-processing
        # ==========================================================

        self.postprocessor = OCRPostProcessor(
            min_confidence=0.70
        )

        self.reconstructor = TextReconstructor()

        # ==========================================================
        # LLM components
        # ==========================================================

        self.groq = GroqClient()

        self.extractor = FieldExtractor(
            self.groq
        )

        # ==========================================================
        # Validation
        # ==========================================================

        self.validator = Validator()

        self.normalizer = Normalizer()

        self.database_connection = DatabaseConnection()

        self.database_manager = DatabaseManager(database_connection=self.database_connection)

    def run(self) -> dict:
        """
        Execute the complete document processing pipeline.

        Returns
        -------
        dict
            Dictionary containing:

            - pages:
                Page-level OCR and processing results.

            - fields:
                Structured banking fields extracted from
                the complete document.

            - validation:
                Validation results for the extracted fields.
        """

        self.database_manager.initialize_database()

        # ==========================================================
        # Step 1 - Validate the input document
        # ==========================================================

        self.loader.validate()

        print(
            "✓ Document validation successful."
        )

        # ==========================================================
        # Step 2 - Convert the PDF into page images
        # ==========================================================

        pages = self.converter.convert()

        print(
            f"✓ PDF converted into {len(pages)} page(s)."
        )

        processed_pages = []

        # ==========================================================
        # Step 3 - Process each page independently
        # ==========================================================

        for page_number, page in enumerate(
            pages,
            start=1
        ):

            print(
                f"\n========== Processing page {page_number} =========="
            )

            # ------------------------------------------------------
            # 3.1 Image preprocessing
            # ------------------------------------------------------

            gray_image = self.grayscale.convert(
                page
            )

            deskewed_image = self.deskew.correct(
                gray_image
            )

            denoised_image = self.denoiser.denoise(
                deskewed_image
            )

            contrast_image = self.contrast.enhance(
                denoised_image
            )

            resized_image = self.resizer.resize(
                contrast_image
            )

            # ------------------------------------------------------
            # 3.2 OCR
            # ------------------------------------------------------

            ocr_results = self.ocr.recognize(
                resized_image
            )

            # ------------------------------------------------------
            # 3.3 OCR post-processing
            # ------------------------------------------------------

            ocr_results = self.postprocessor.filter_confidence(
                ocr_results
            )

            ocr_results = self.postprocessor.sort_reading_order(
                ocr_results
            )

            # ------------------------------------------------------
            # 3.4 Text reconstruction
            # ------------------------------------------------------

            reconstructed_lines = self.reconstructor.reconstruct(
                ocr_results
            )

            ocr_text = "\n".join(
                reconstructed_lines
            )

            # ------------------------------------------------------
            # 3.5 OCR correction
            # ------------------------------------------------------

            corrected_text = self.groq.correct_ocr(
                ocr_text
            )

            # ======================================================
            # Step 4 - Save intermediate results
            # ======================================================

            if self.save_intermediate:

                gray_path = (
                    self.output_dir
                    / f"page_{page_number}_gray.png"
                )

                deskew_path = (
                    self.output_dir
                    / f"page_{page_number}_deskew.png"
                )

                denoise_path = (
                    self.output_dir
                    / f"page_{page_number}_denoised.png"
                )

                contrast_path = (
                    self.output_dir
                    / f"page_{page_number}_contrast.png"
                )

                resize_path = (
                    self.output_dir
                    / f"page_{page_number}_resized.png"
                )

                ocr_json_path = (
                    self.output_dir
                    / f"page_{page_number}_ocr.json"
                )

                cv2.imwrite(
                    str(gray_path),
                    gray_image
                )

                cv2.imwrite(
                    str(deskew_path),
                    deskewed_image
                )

                cv2.imwrite(
                    str(denoise_path),
                    denoised_image
                )

                cv2.imwrite(
                    str(contrast_path),
                    contrast_image
                )

                cv2.imwrite(
                    str(resize_path),
                    resized_image
                )

                with open(
                    ocr_json_path,
                    "w",
                    encoding="utf-8"
                ) as file:

                    json.dump(
                        ocr_results,
                        file,
                        indent=4,
                        ensure_ascii=False
                    )

                print(
                    f"✓ Saved: {gray_path.name}"
                )

                print(
                    f"✓ Saved: {deskew_path.name}"
                )

                print(
                    f"✓ Saved: {denoise_path.name}"
                )

                print(
                    f"✓ Saved: {contrast_path.name}"
                )

                print(
                    f"✓ Saved: {resize_path.name}"
                )

                print(
                    f"✓ Saved: {ocr_json_path.name}"
                )

            # ======================================================
            # Step 5 - Store page processing results
            # ======================================================

            processed_pages.append(
                {
                    "image": resized_image,
                    "ocr": ocr_results,
                    "lines": reconstructed_lines,
                    "corrected_text": corrected_text,
                }
            )

        # ==========================================================
        # Step 6 - Collect corrected text from all pages
        # ==========================================================

        corrected_pages = [
            page["corrected_text"]
            for page in processed_pages
        ]

        # ==========================================================
        # Step 7 - Extract structured banking fields
        # ==========================================================

        extracted_fields = self.extractor.extract(
            corrected_pages
        )

        print(
            "\n===== Extracted Fields =====\n"
        )

        print(
            json.dumps(
                extracted_fields,
                indent=4,
                ensure_ascii=False
            )
        )

        # ==========================================================
        # Step 8 - Validate extracted fields
        # ==========================================================

        validation_result = self.validator.validate(
            extracted_fields
        )

        print(
            "\n===== Validation Results =====\n"
        )

        print(
            json.dumps(
                validation_result,
                indent=4,
                ensure_ascii=False
            )
        )

        # ==========================================================
        # Stepp 9 - Normalization
        # ==========================================================

        normalized_fields = self.normalizer.normalize(extracted_fields)

        dossier_id = self.database_manager.save_credit_dossier(normalized_fields)

        # ==========================================================
        # Pipeline completed
        # ==========================================================

        print(
            "\n✓ Document processing pipeline completed successfully."
        )

        return {
            "pages": processed_pages,
            "fields": extracted_fields,
            "validation": validation_result,
            "normalized_fields": normalized_fields,
            "dossier_id": dossier_id,
        }