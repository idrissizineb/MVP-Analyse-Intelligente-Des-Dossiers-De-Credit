import cv2
import numpy as np


class ImageResizer:
    """
    Resize document images while preserving
    the original aspect ratio.
    """

    def __init__(
        self,
        target_longest_side: int = 2500
    ):
        """
        Initialize the image resizer.

        Parameters
        ----------
        target_longest_side : int
            Desired size (in pixels) of the longest side.
        """

        if target_longest_side <= 0:
            raise ValueError(
                "'target_longest_side' must be greater than zero."
            )

        self.target_longest_side = target_longest_side

    def resize(
        self,
        image: np.ndarray
    ) -> np.ndarray:
        """
        Resize an image while preserving its aspect ratio.

        Parameters
        ----------
        image : np.ndarray
            Input grayscale image.

        Returns
        -------
        np.ndarray
            Resized image.
        """

        height, width = image.shape[:2]

        longest_side = max(height, width)

        # No resizing needed
        if longest_side >= self.target_longest_side:
            return image

        # Compute scaling factor
        scale = self.target_longest_side / longest_side

        # Compute new dimensions
        new_width = int(width * scale)
        new_height = int(height * scale)

        # Resize using high-quality interpolation
        resized = cv2.resize(
            image,
            (new_width, new_height),
            interpolation=cv2.INTER_LANCZOS4
        )

        return resized