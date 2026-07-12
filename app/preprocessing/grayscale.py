from PIL import Image
import numpy as np
import cv2

class GrayscaleConverter:
    """
    Convert a PIL image to grayscale.

    Responsibilities:
        - Receive a PIL Image
        - Convert it to OpenCV format
        - Convert it to grayscale
        - Return the grayscale image
    """

    def convert(self, image: Image) -> np.ndarray:
        """
        Convert a PIL image to grayscale.

        Parameters
        ----------
        image : PIL.Image.Image
            Input image.

        Returns
        -------
        numpy.ndarray
            Grayscale image.
        """
        # Convert PIL → NumPy
        image_np = np.array(image)

        # Convert RGB → BGR
        image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

        # Convert BGR → Grayscale
        gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

        return gray