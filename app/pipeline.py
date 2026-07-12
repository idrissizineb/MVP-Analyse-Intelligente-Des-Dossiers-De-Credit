from pathlib import Path

import cv2
import numpy as np

from app.preprocessing.loader import DocumentLoader
from app.preprocessing.pdf_converter import PDFConverter
from app.preprocessing.grayscale import GrayscaleConverter
from app.preprocessing.deskew import DeskewCorrector
from app.preprocessing.denoise import Denoiser
from app.preprocessing.contrast import ContrastEnhancer
from app.preprocessing.resize import ImageResizer


class DocumentPipeline:
    """
    End-to-end preprocessing pipeline for banking documents.

    Pipeline:
        1. Validate document
        2. Convert PDF to images
        3. Convert to grayscale
        4. Correct document skew
        5. Remove image noise
        6. Enhance contrast using CLAHE
        7. Resize image for OCR
        8. Save intermediate results (optional)

    Future additions:
        - PaddleOCR
        - Document classification
        - Field extraction
        - Data validation
        - Database storage
    """

    def __init__(
        self,
        pdf_path: str,
        output_dir: str = "data/processed",
        save_intermediate: bool = True,
    ):
        """
        Initialize the preprocessing pipeline.

        Parameters
        ----------
        pdf_path : str
            Path to the input PDF document.

        output_dir : str
            Directory where processed images will be saved.

        save_intermediate : bool
            Whether to save every preprocessing step.
        """

        # -------------------------------
        # Configuration
        # -------------------------------
        self.pdf_path = pdf_path
        self.output_dir = Path(output_dir)
        self.save_intermediate = save_intermediate

        self.output_dir.mkdir(parents=True, exist_ok=True)

        # -------------------------------
        # Initialize preprocessing modules
        # -------------------------------
        self.loader = DocumentLoader(self.pdf_path)
        self.converter = PDFConverter(self.pdf_path)
        self.grayscale = GrayscaleConverter()
        self.deskew = DeskewCorrector()
        self.denoiser = Denoiser(method="nlm")
        self.contrast = ContrastEnhancer()
        self.resizer = ImageResizer(target_longest_side=2500)

    def run(self) -> list[np.ndarray]:
        """
        Execute the preprocessing pipeline.

        Returns
        -------
        list[np.ndarray]
            List of processed document pages.
        """

        # ==========================================================
        # Step 1 - Validate input document
        # ==========================================================
        self.loader.validate()
        print("✓ Document validation successful.")

        # ==========================================================
        # Step 2 - Convert PDF into images
        # ==========================================================
        pages = self.converter.convert()
        print(f"✓ PDF converted into {len(pages)} page(s).")

        processed_pages = []

        # ==========================================================
        # Step 3 - Process every page
        # ==========================================================
        for page_number, page in enumerate(pages, start=1):

            print(f"\n========== Processing page {page_number} ==========")

            # ------------------------------------------------------
            # Image preprocessing
            # ------------------------------------------------------

            gray_image = self.grayscale.convert(page)

            deskewed_image = self.deskew.correct(gray_image)

            denoised_image = self.denoiser.denoise(deskewed_image)

            contrast_image = self.contrast.enhance(denoised_image)

            resized_image = self.resizer.resize(contrast_image)

            # ------------------------------------------------------
            # Save intermediate images (development mode)
            # ------------------------------------------------------

            if self.save_intermediate:

                gray_path = self.output_dir / f"page_{page_number}_gray.png"
                deskew_path = self.output_dir / f"page_{page_number}_deskew.png"
                denoise_path = self.output_dir / f"page_{page_number}_denoised.png"
                contrast_path = self.output_dir / f"page_{page_number}_contrast.png"
                resize_path = self.output_dir / f"page_{page_number}_resized.png"

                cv2.imwrite(str(gray_path), gray_image)
                cv2.imwrite(str(deskew_path), deskewed_image)
                cv2.imwrite(str(denoise_path), denoised_image)
                cv2.imwrite(str(contrast_path), contrast_image)
                cv2.imwrite(str(resize_path), resized_image)

                print(f"✓ Saved: {gray_path.name}")
                print(f"✓ Saved: {deskew_path.name}")
                print(f"✓ Saved: {denoise_path.name}")
                print(f"✓ Saved: {contrast_path.name}")
                print(f"✓ Saved: {resize_path.name}")

            # ------------------------------------------------------
            # Store final processed page
            # ------------------------------------------------------

            processed_pages.append(resized_image)

        # ==========================================================
        # Pipeline completed
        # ==========================================================

        print("\n✓ Preprocessing completed successfully.")

        return processed_pages