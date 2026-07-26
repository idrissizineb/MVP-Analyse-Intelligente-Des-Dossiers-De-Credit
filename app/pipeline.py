from pathlib import Path
import cv2
import json


# ==========================================================
# PREPROCESSING
# ==========================================================

from app.preprocessing.loader import DocumentLoader
from app.preprocessing.pdf_converter import PDFConverter
from app.preprocessing.grayscale import GrayscaleConverter
from app.preprocessing.deskew import DeskewCorrector
from app.preprocessing.denoise import Denoiser
from app.preprocessing.contrast import ContrastEnhancer
from app.preprocessing.resize import ImageResizer


# ==========================================================
# OCR
# ==========================================================

from app.ocr.paddle_ocr import PaddleOCRProcessor


# ==========================================================
# POSTPROCESSING
# ==========================================================

from app.postprocessing.ocr_postprocessor import OCRPostProcessor
from app.postprocessing.text_reconstructor import TextReconstructor


# ==========================================================
# LLM
# ==========================================================

from app.llm.groq_client import GroqClient
from app.llm.field_extractor import FieldExtractor


# ==========================================================
# VALIDATION & NORMALIZATION
# ==========================================================

from app.validation.validator import Validator
from app.normalization.normalizer import Normalizer


# ==========================================================
# DATABASE
# ==========================================================

from data.database.connection import DatabaseConnection
from data.database.database_manager import DatabaseManager


class DocumentPipeline:
    """
    End-to-end Intelligent Document Processing pipeline
    for banking documents.

    Pipeline:

        1. Validate the input document
        2. Convert PDF into page images
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
        14. Validate extracted fields
        15. Normalize extracted fields
        16. Store data in the database
        17. Return processing results
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
            Directory used to save intermediate files.

        save_intermediate : bool
            Whether to save intermediate images and OCR results.
        """

        # ======================================================
        # CONFIGURATION
        # ======================================================

        self.pdf_path = Path(pdf_path)

        self.output_dir = Path(output_dir)

        self.save_intermediate = save_intermediate

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        # ======================================================
        # DOCUMENT LOADING
        # ======================================================

        self.loader = DocumentLoader(
            str(self.pdf_path)
        )

        self.converter = PDFConverter(
            str(self.pdf_path)
        )

        # ======================================================
        # IMAGE PREPROCESSING
        # ======================================================

        self.grayscale = GrayscaleConverter()

        self.deskew = DeskewCorrector()

        self.denoiser = Denoiser(
            method="nlm"
        )

        self.contrast = ContrastEnhancer()

        self.resizer = ImageResizer(
            target_longest_side=2500
        )

        # ======================================================
        # OCR
        # ======================================================

        self.ocr = PaddleOCRProcessor()

        # ======================================================
        # OCR POSTPROCESSING
        # ======================================================

        self.postprocessor = OCRPostProcessor(
            min_confidence=0.70
        )

        self.reconstructor = TextReconstructor()

        # ======================================================
        # LLM
        # ======================================================

        self.groq = GroqClient()

        self.extractor = FieldExtractor(
            self.groq
        )

        # ======================================================
        # VALIDATION
        # ======================================================

        self.validator = Validator()

        self.normalizer = Normalizer()

        # ======================================================
        # DATABASE
        # ======================================================

        self.database_connection = DatabaseConnection()

        self.database_manager = DatabaseManager(
            database_connection=self.database_connection
        )

    # ==========================================================
    # SAVE IMAGE
    # ==========================================================

    def _save_image(
        self,
        image,
        filename: str
    ) -> str:

        """
        Save an image to the output directory.

        Returns
        -------
        str
            Path to the saved image.
        """

        image_path = self.output_dir / filename

        success = cv2.imwrite(
            str(image_path),
            image
        )

        if not success:

            raise IOError(
                f"Failed to save image: {image_path}"
            )

        return str(image_path)

    # ==========================================================
    # SAVE JSON
    # ==========================================================

    def _save_json(
        self,
        data,
        filename: str
    ) -> str:

        """
        Save data as JSON.

        Returns
        -------
        str
            Path to the saved JSON file.
        """

        json_path = self.output_dir / filename

        with open(
            json_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False
            )

        return str(json_path)

    # ==========================================================
    # PROCESS SINGLE PAGE
    # ==========================================================

    def _process_page(
        self,
        page,
        page_number: int
    ) -> dict:

        """
        Process a single PDF page.

        Returns
        -------
        dict
            Page processing results.
        """

        print(
            f"\n========== Processing page {page_number} =========="
        )

        # ======================================================
        # IMAGE PREPROCESSING
        # ======================================================

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

        # ======================================================
        # OCR
        # ======================================================

        ocr_results = self.ocr.recognize(
            resized_image
        )

        # ======================================================
        # OCR POSTPROCESSING
        # ======================================================

        filtered_ocr_results = self.postprocessor.filter_confidence(
            ocr_results
        )

        sorted_ocr_results = self.postprocessor.sort_reading_order(
            filtered_ocr_results
        )

        # ======================================================
        # TEXT RECONSTRUCTION
        # ======================================================

        reconstructed_lines = self.reconstructor.reconstruct(
            sorted_ocr_results
        )

        reconstructed_text = "\n".join(
            reconstructed_lines
        )

        print(
            "\n===== Reconstructed Document ====="
        )

        for index, line in enumerate(
            reconstructed_lines,
            start=1
        ):

            print(
                f"{index:02d}. {line}"
            )

        # ======================================================
        # OCR CORRECTION USING LLM
        # ======================================================

        try:

            corrected_text = self.groq.correct_ocr(
                reconstructed_text
            )

        except Exception as error:

            print(
                f"⚠ OCR correction failed: {error}"
            )

            print(
                "Using reconstructed OCR text instead."
            )

            corrected_text = reconstructed_text

        # ======================================================
        # SAVE INTERMEDIATE RESULTS
        # ======================================================

        resized_path = None

        if self.save_intermediate:

            gray_path = self._save_image(
                gray_image,
                f"page_{page_number}_gray.png"
            )

            deskew_path = self._save_image(
                deskewed_image,
                f"page_{page_number}_deskew.png"
            )

            denoise_path = self._save_image(
                denoised_image,
                f"page_{page_number}_denoised.png"
            )

            contrast_path = self._save_image(
                contrast_image,
                f"page_{page_number}_contrast.png"
            )

            resized_path = self._save_image(
                resized_image,
                f"page_{page_number}_resized.png"
            )

            ocr_json_path = self._save_json(
                sorted_ocr_results,
                f"page_{page_number}_ocr.json"
            )

            reconstructed_text_path = self._save_json(
                {
                    "text": reconstructed_text
                },
                f"page_{page_number}_reconstructed.json"
            )

            corrected_text_path = self._save_json(
                {
                    "text": corrected_text
                },
                f"page_{page_number}_corrected.json"
            )

            print(
                f"✓ Saved: {gray_path}"
            )

            print(
                f"✓ Saved: {deskew_path}"
            )

            print(
                f"✓ Saved: {denoise_path}"
            )

            print(
                f"✓ Saved: {contrast_path}"
            )

            print(
                f"✓ Saved: {resized_path}"
            )

            print(
                f"✓ Saved: {ocr_json_path}"
            )

            print(
                f"✓ Saved: {reconstructed_text_path}"
            )

            print(
                f"✓ Saved: {corrected_text_path}"
            )

        # ======================================================
        # RETURN CLEAN PAGE RESULT
        # ======================================================

        return {

            "page_number": page_number,

            "resized_path": resized_path,

            "ocr": sorted_ocr_results,

            "lines": reconstructed_lines,

            "reconstructed_text": reconstructed_text,

            "corrected_text": corrected_text,

        }

    # ==========================================================
    # RUN PIPELINE
    # ==========================================================

    def run(self) -> dict:

        """
        Execute the complete document processing pipeline.

        Returns
        -------
        dict
            Complete document processing results.
        """

        # ======================================================
        # DATABASE INITIALIZATION
        # ======================================================

        self.database_manager.initialize_database()

        # ======================================================
        # STEP 1 - VALIDATE DOCUMENT
        # ======================================================

        self.loader.validate()

        print(
            "\n✓ Document validation successful."
        )

        # ======================================================
        # STEP 2 - CONVERT PDF
        # ======================================================

        pages = self.converter.convert()

        print(
            f"✓ PDF converted into {len(pages)} page(s)."
        )

        # ======================================================
        # STEP 3 - PROCESS EACH PAGE
        # ======================================================

        processed_pages = []

        for page_number, page in enumerate(
            pages,
            start=1
        ):

            processed_page = self._process_page(
                page,
                page_number
            )

            processed_pages.append(
                processed_page
            )

        # ======================================================
        # STEP 4 - COLLECT CORRECTED TEXT
        # ======================================================

        corrected_pages = [

            page["corrected_text"]

            for page in processed_pages

        ]

        # ======================================================
        # STEP 5 - EXTRACT FIELDS
        # ======================================================

        extracted_fields = self.extractor.extract(
            corrected_pages
        )

        print(
            "\n========== EXTRACTED FIELDS ==========\n"
        )

        print(
            json.dumps(
                extracted_fields,
                indent=4,
                ensure_ascii=False
            )
        )

        # ======================================================
        # STEP 6 - VALIDATE FIELDS
        # ======================================================

        validation_result = self.validator.validate(
            extracted_fields
        )

        print(
            "\n========== VALIDATION RESULTS ==========\n"
        )

        print(
            json.dumps(
                validation_result,
                indent=4,
                ensure_ascii=False
            )
        )

        # ======================================================
        # STEP 7 - NORMALIZE FIELDS
        # ======================================================

        normalized_fields = self.normalizer.normalize(
            extracted_fields
        )

        print(
            "\n========== NORMALIZED FIELDS ==========\n"
        )

        print(
            json.dumps(
                normalized_fields,
                indent=4,
                ensure_ascii=False,
                default=str
            )
        )

        # ======================================================
        # STEP 8 - SAVE CREDIT DOSSIER
        # ======================================================

        dossier_id = self.database_manager.save_credit_dossier(
            normalized_fields
        )

        print(
            "\n========== DATABASE =========="
        )

        print(
            f"Credit dossier saved successfully."
        )

        print(
            f"Dossier ID: {dossier_id}"
        )

        # ======================================================
        # STEP 9 - CREATE DOCUMENT
        # ======================================================

        document_id = self.database_manager.create_document(

            dossier_id=dossier_id,

            nom_fichier=self.pdf_path.name,

            type_document=None,

            nombre_pages=len(processed_pages),

            chemin_fichier=str(self.pdf_path)

        )

        print(
            f"Document ID: {document_id}"
        )

        # ======================================================
        # STEP 10 - SAVE DOCUMENT PAGES
        # ======================================================

        page_ids = []

        print(
            "\n========== SAVING DOCUMENT PAGES =========="
        )

        for page in processed_pages:

            page_number = page["page_number"]

            print(
                f"\nSaving page {page_number}..."
            )

            resized_path = page["resized_path"]

            if resized_path is None:

                print(
                    f"⚠ No saved image path for page {page_number}"
                )

                continue

            page_id = self.database_manager.create_document_page(

                document_id=document_id,

                numero_page=page_number,

                chemin_image=resized_path

            )

            page_ids.append(
                page_id
            )

            print(
                f"✓ Page {page_number} saved successfully."
            )

            print(
                f"✓ Page ID: {page_id}"
            )

        # ======================================================
        # FINAL RESULT
        # ======================================================

        print(
            "\n✓ Document processing pipeline completed successfully."
        )

        return {

            "pages": processed_pages,

            "fields": extracted_fields,

            "validation": validation_result,

            "normalized_fields": normalized_fields,

            "dossier_id": dossier_id,

            "document_id": document_id,

            "page_ids": page_ids

        }