import cv2
import numpy as np


class ContrastEnhancer:
    """
    Enhance the contrast of grayscale document images using CLAHE.
    """

    def __init__(
        self,
        clip_limit: float = 1.5,
        tile_grid_size: tuple[int, int] = (8, 8),
    ):
        """
        Initialize the CLAHE contrast enhancer.

        Parameters
        ----------
        clip_limit : float
            Limits the amount of local contrast enhancement.

        tile_grid_size : tuple[int, int]
            Number of tiles in the horizontal and vertical directions.
        """

        if clip_limit <= 0:
            raise ValueError(
                "'clip_limit' must be greater than zero."
            )

        if (
            len(tile_grid_size) != 2
            or tile_grid_size[0] <= 0
            or tile_grid_size[1] <= 0
        ):
            raise ValueError(
                "'tile_grid_size' must contain two positive integers."
            )

        self.clip_limit = clip_limit
        self.tile_grid_size = tile_grid_size

        self.clahe = cv2.createCLAHE(
            clipLimit=self.clip_limit,
            tileGridSize=self.tile_grid_size,
        )

    def enhance(self, image: np.ndarray) -> np.ndarray:
        """
        Apply CLAHE to a grayscale image.

        Parameters
        ----------
        image : np.ndarray
            Grayscale image.

        Returns
        -------
        np.ndarray
            Contrast-enhanced image.
        """

        enhanced = self.clahe.apply(image)

        return enhanced