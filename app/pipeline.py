from pathlib import Path

import cv2
import json
import numpy as np

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


class DocumentPipeline:
    """
    End-to-end Intelligent Document Processing pipeline
    for banking documents.

    Pipeline:
        1. Validate the input document
        2. Convert the PDF into individual page images
        3. Convert images to grayscale
        4. Correct document skew
        5. Remove image noise
        6. Enhance image contrast using CLAHE
        7. Resize images for OCR

        8. Perform OCR using PaddleOCR

        9. Filter OCR results according to confidence scores
       10. Sort detected text according to reading order
       11. Reconstruct the detected text into readable lines

       12. Correct OCR errors using Groq
       13. Merge corrected text from all document pages
       14. Extract structured banking fields using Groq
       15. Return page-level OCR data and document-level fields

    Current output:
        - Processed page images
        - Raw OCR results
        - Reconstructed OCR text
        - Corrected OCR text
        - Extracted structured banking fields
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
            Directory where intermediate processing results
            will be saved.

        save_intermediate : bool
            Whether to save intermediate images and OCR results.
        """

        # ==========================================================
        # Configuration
        # ==========================================================

        self.pdf_path = pdf_path

        self.output_dir = Path(output_dir)

        self.save_intermediate = save_intermediate

        # Create the output directory if it does not already exist.
        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        # ==========================================================
        # Initialize document loading and PDF conversion modules
        # ==========================================================

        self.loader = DocumentLoader(
            self.pdf_path
        )

        self.converter = PDFConverter(
            self.pdf_path
        )

        # ==========================================================
        # Initialize image preprocessing modules
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
        # Initialize OCR module
        # ==========================================================

        self.ocr = PaddleOCRProcessor()

        # ==========================================================
        # Initialize OCR post-processing modules
        # ==========================================================

        # Keep only OCR detections whose confidence score
        # is at least 70%.
        self.postprocessor = OCRPostProcessor(
            min_confidence=0.70
        )

        # Reconstruct individual OCR detections into
        # readable text lines.
        self.reconstructor = TextReconstructor()

        # ==========================================================
        # Initialize LLM modules
        # ==========================================================

        # One shared Groq client is used by the different
        # LLM-based components.
        self.groq = GroqClient()

        # The field extractor receives the shared Groq client.
        self.extractor = FieldExtractor(
            self.groq
        )

    def run(self) -> dict:
        """
        Execute the complete document processing pipeline.

        Returns
        -------
        dict
            A dictionary containing:

            - "pages":
                Page-level processing results, including:
                images, OCR results, reconstructed lines,
                and corrected OCR text.

            - "fields":
                Structured banking information extracted
                from the complete document.
        """

        # ==========================================================
        # Step 1 - Validate the input document
        # ==========================================================

        self.loader.validate()

        print(
            "✓ Document validation successful."
        )

        # ==========================================================
        # Step 2 - Convert the PDF into individual page images
        # ==========================================================

        pages = self.converter.convert()

        print(
            f"✓ PDF converted into {len(pages)} page(s)."
        )

        # This list will store the complete processing result
        # for every page.
        processed_pages = []

        # ==========================================================
        # Step 3 - Process every page independently
        # ==========================================================

        for page_number, page in enumerate(
            pages,
            start=1
        ):

            print(
                f"\n========== Processing page {page_number} =========="
            )

            # ------------------------------------------------------
            # Step 3.1 - Image preprocessing
            # ------------------------------------------------------

            # Convert the page image to grayscale.
            gray_image = self.grayscale.convert(
                page
            )

            # Correct the document's geometric skew.
            deskewed_image = self.deskew.correct(
                gray_image
            )

            # Reduce image noise while preserving text details.
            denoised_image = self.denoiser.denoise(
                deskewed_image
            )

            # Enhance local image contrast using CLAHE.
            contrast_image = self.contrast.enhance(
                denoised_image
            )

            # Resize the image to an appropriate resolution
            # for OCR processing.
            resized_image = self.resizer.resize(
                contrast_image
            )

            # ------------------------------------------------------
            # Step 3.2 - OCR
            # ------------------------------------------------------

            # Detect and recognize text using PaddleOCR.
            ocr_results = self.ocr.recognize(
                resized_image
            )

            # ------------------------------------------------------
            # Step 3.3 - OCR post-processing
            # ------------------------------------------------------

            # Remove low-confidence OCR detections.
            ocr_results = self.postprocessor.filter_confidence(
                ocr_results
            )

            # Sort the remaining OCR detections according
            # to their spatial reading order.
            ocr_results = self.postprocessor.sort_reading_order(
                ocr_results
            )

            # ------------------------------------------------------
            # Step 3.4 - Text reconstruction
            # ------------------------------------------------------

            # Reconstruct individual OCR detections into
            # readable text lines.
            reconstructed_lines = self.reconstructor.reconstruct(
                ocr_results
            )

            # ------------------------------------------------------
            # Step 3.5 - Convert reconstructed lines into one
            # text block
            # ------------------------------------------------------

            ocr_text = "\n".join(
                reconstructed_lines
            )

            # ------------------------------------------------------
            # Step 3.6 - Correct OCR errors using Groq
            # ------------------------------------------------------

            # Groq corrects linguistic and formatting errors
            # while preserving the original information.
            corrected_text = self.groq.correct_ocr(
                ocr_text
            )

            # ======================================================
            # Step 4 - Save intermediate processing results
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

                # Save intermediate images.

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

                # Save the final OCR detections after
                # confidence filtering and reading-order sorting.
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
                    f"✓ Saved: {ocr_json_path.name}"
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

            # ======================================================
            # Step 5 - Store the processed page
            # ======================================================

            processed_pages.append(
                {
                    # Preprocessed image used by PaddleOCR.
                    "image": resized_image,

                    # OCR detections after confidence filtering
                    # and reading-order sorting.
                    "ocr": ocr_results,

                    # Text reconstructed from OCR detections.
                    "lines": reconstructed_lines,

                    # Text corrected by the Groq OCR
                    # post-processing stage.
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
        # Step 7 - Extract structured fields from the complete
        # document
        # ==========================================================

        # The corrected text from all pages is sent to the
        # field extraction module.
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
        # Pipeline completed
        # ==========================================================

        print(
            "\n✓ Document processing pipeline completed successfully."
        )

        # Return both page-level processing results and
        # document-level extracted fields.
        return {
            "pages": processed_pages,
            "fields": extracted_fields,
        }