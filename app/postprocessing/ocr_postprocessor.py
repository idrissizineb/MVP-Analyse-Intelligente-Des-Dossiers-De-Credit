from typing import List


class OCRPostProcessor:
    """
    Post-process OCR results to improve their quality before
    passing them to downstream modules.

    Current features
    ----------------
    - Confidence filtering

    Future features
    ---------------
    - Duplicate removal
    - Reading-order sorting
    - Line reconstruction
    - Paragraph reconstruction
    """

    def __init__(self, min_confidence: float = 0.70):
        """
        Initialize the OCR post-processor.

        Parameters
        ----------
        min_confidence : float
            Minimum confidence required to keep an OCR detection.
        """

        self.min_confidence = min_confidence

    def filter_confidence(self, ocr_results: List[dict]) -> List[dict]:
        """
        Remove OCR detections whose confidence score is
        below the configured threshold.

        Parameters
        ----------
        ocr_results : List[dict]
            Raw OCR results produced by PaddleOCR.

        Returns
        -------
        List[dict]
            Filtered OCR results.
        """

        filtered_results = []

        removed = 0

        for result in ocr_results:

            confidence = result["confidence"]

            if confidence >= self.min_confidence:
                filtered_results.append(result)
            else:
                removed += 1

        print("\n===== OCR Confidence Filtering =====")
        print(f"Initial detections : {len(ocr_results)}")
        print(f"Removed detections : {removed}")
        print(f"Remaining detections : {len(filtered_results)}")

        return filtered_results