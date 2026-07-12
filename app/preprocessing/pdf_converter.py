# Convert each PDF page into an image.

from pathlib import Path
from typing import List
from app.config import POPPLER_PATH
from pdf2image import convert_from_path
from PIL import Image


class PDFConverter:
    """
    Converts a PDF document into a list of PIL images.

    Responsibilities:
        - Validate that the file is a PDF.
        - Convert every page into a PIL Image.
        - Return the images.

    This class DOES NOT:
        - preprocess images
        - perform OCR
        - save to database
    """

    def __init__(self, pdf_path: str | Path):
        self.pdf_path = Path(pdf_path)

    def convert(self, dpi: int = 300) -> List[Image.Image]:
        """
        Convert the PDF into PIL Images.

        Parameters
        ----------
        dpi : int
            Resolution used during conversion.

        Returns
        -------
        List[PIL.Image.Image]
            One image per page.
        """

        if self.pdf_path.suffix.lower() != ".pdf":
            raise ValueError(
                "PDFConverter only accepts PDF files."
            )

        images = convert_from_path(
            self.pdf_path,
            dpi=dpi,
            poppler_path=POPPLER_PATH
        )

        return images