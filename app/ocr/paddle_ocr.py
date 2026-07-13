from paddleocr import PaddleOCR  # pyright: ignore[reportMissingImports]
import numpy as np


class PaddleOCRProcessor:
    """
    Wrapper around PaddleOCR for text detection and recognition.
    """

    def __init__(
        self,
        language: str = "fr",
        use_gpu: bool = False,
        use_angle_cls: bool = True,
    ):
        """
        Initialize the PaddleOCR engine.

        Parameters
        ----------
        language : str
            OCR language.

        use_gpu : bool
            Whether to use GPU acceleration.

        use_angle_cls : bool
            Enable angle classification for rotated text.
        """

        print("Loading PaddleOCR model...")

        self.ocr = PaddleOCR(
            lang=language,
            use_gpu=use_gpu,
            use_angle_cls=use_angle_cls,
        )

        print("PaddleOCR model loaded successfully.")

    def recognize(self, image: np.ndarray) -> list[dict]:
        """
        Perform OCR on a preprocessed image.

        Parameters
        ----------
        image : np.ndarray
            Preprocessed OpenCV image.

        Returns
        -------
        list[dict]
            OCR results.
        """

        results = self.ocr.ocr(image, cls=True)

        extracted_results = []

        if not results or not results[0]:
            return extracted_results

        for line in results[0]:

            polygon = line[0]
            text = line[1][0]
            confidence = float(line[1][1])

            extracted_results.append(
                {
                    "text": text,
                    "confidence": confidence,
                    "polygon": polygon,
                }
            )

        return extracted_results