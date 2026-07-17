from typing import List


class OCRPostProcessor:
    """
    Post-process OCR results to improve their quality before
    passing them to downstream modules.

    Current features
    ----------------
    - Confidence filtering
    - Reading-order sorting
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

    def sort_reading_order(self, ocr_results: list[dict]) -> list[dict]:
        """
        Sort OCR detections in natural reading order.

        Reading order:
            1. Top to bottom (y coordinate)
            2. Left to right (x coordinate)

        Parameters
        ----------
        ocr_results : list[dict]
            OCR detections after confidence filtering.

        Returns
        -------
        list[dict]
            OCR detections sorted in reading order.
        """
        # ---------------------------------------------------------
# Sort OCR detections into natural reading order

# 1. Compare the vertical position (y-coordinate).
#    - If y1 < y2:
#         → Detection 1 comes first (higher on the page).
#    - If y1 > y2:
#         → Detection 2 comes first.
#
# 2. If both detections belong to the same text line
#    (their y-coordinates are equal or within a small tolerance),
#    compare their horizontal position (x-coordinate).
#    - If x1 < x2:
#         → Detection 1 comes first (left to right).
#    - If x1 > x2:
#         → Detection 2 comes first.
#
# Final reading order:
#     Top → Bottom
#     Left → Right (within each line)
# ---------------------------------------------------------

        sorted_results = sorted(
            ocr_results,
            key=lambda result: (
                result["polygon"][0][1],   # y coordinate
                result["polygon"][0][0]    # x coordinate
            )
        )

        print("\n===== Reading Order =====")

        for i, result in enumerate(sorted_results, start=1):
            print(f"{i:02d}. {result['text']}")

        return sorted_results