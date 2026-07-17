from typing import List


class TextReconstructor:
    """
    Reconstruct human-readable document lines from OCR detections.

    The OCR detections are assumed to be already:
        1. Filtered by confidence
        2. Sorted in reading order

    This class groups words that belong to the same horizontal line,
    sorts them from left to right, and reconstructs complete text lines.
    """

    def __init__(self, line_tolerance: int = 15):
        """
        Initialize the text reconstructor.

        Parameters
        ----------
        line_tolerance : int
            Maximum vertical distance (pixels) between two OCR detections
            to consider them part of the same text line.
        """
        self.line_tolerance = line_tolerance

# ---------------------------------------------------------
# Reconstruct document lines from OCR detections.
#
# Logic:
#
# 1. Start a new line with the first OCR detection.
#
# 2. For each subsequent detection:
#    - Compare its y-coordinate with the current line's y-coordinate.
#
#    - If the vertical difference is smaller than a predefined
#      tolerance (e.g., 10 pixels), the detection is considered
#      part of the same text line and its text is appended to the
#      current line.
#
#    - Otherwise, the current line is complete:
#         • Save the reconstructed line.
#         • Start a new line with the current detection.
#
# 3. After all detections have been processed, save the last line.
#
# 4. Finally, join all reconstructed lines using newline characters
#    ('\n') to recreate the document in a human-readable format.
#
# This step transforms individual OCR words into complete text lines,
# making the output easier to read and better suited for subsequent
# processing by the Groq language model.
# ---------------------------------------------------------


    def reconstruct(self, ocr_results: List[dict]) -> List[str]:
        """
        Reconstruct readable document lines from OCR detections.

        Parameters
        ----------
        ocr_results : List[dict]
            OCR detections.

        Returns
        -------
        List[str]
            Reconstructed document lines.
        """

        if not ocr_results:
            return []

        # ==========================================================
        # Step 1 - Group detections into lines
        # ==========================================================

        grouped_lines = []

        current_line = [ocr_results[0]]
        current_y = ocr_results[0]["polygon"][0][1]

        for result in ocr_results[1:]:

            y = result["polygon"][0][1]

            if abs(y - current_y) <= self.line_tolerance:
                current_line.append(result)

            else:
                grouped_lines.append(current_line)

                current_line = [result]
                current_y = y

        # Add the last line
        grouped_lines.append(current_line)

        # ==========================================================
        # Step 2 - Sort words inside each line
        # ==========================================================

        reconstructed_lines = []

        for line in grouped_lines:

            line.sort(
                key=lambda word: word["polygon"][0][0]
            )

            line_text = " ".join(
                word["text"] for word in line
            )

            reconstructed_lines.append(line_text)

        # ==========================================================
        # Debug
        # ==========================================================

        print("\n===== Reconstructed Document =====")

        for i, line in enumerate(reconstructed_lines, start=1):
            print(f"{i:02d}. {line}")

        return reconstructed_lines