import cv2
import numpy as np


class DeskewCorrector:
    """
    Detect and correct the skew of scanned document images.

    The class estimates the dominant orientation of near-horizontal
    document structures using the Probabilistic Hough Transform,
    then rotates the image to make it horizontal.
    """

    def __init__(
        self,
        use_blur: bool = True,
        blur_kernel: tuple = (3, 3)
    ):
        """
        Parameters
        ----------
        use_blur : bool
            Apply a small Gaussian blur before edge detection.

        blur_kernel : tuple
            Kernel size used for Gaussian Blur.
        """
        self.use_blur = use_blur
        self.blur_kernel = blur_kernel

    def estimate_angle(self, image: np.ndarray) -> float:
        """
        Estimate the skew angle of a grayscale document.

        Parameters
        ----------
        image : np.ndarray
            Grayscale document image.

        Returns
        -------
        float
            Estimated skew angle in degrees.
        """

        # -------------------------------------------------
        # Optional Gaussian Blur
        # -------------------------------------------------
        if self.use_blur:
            image = cv2.GaussianBlur(
                image,
                self.blur_kernel,
                sigmaX=0
            )

        # -------------------------------------------------
        # Edge Detection
        # -------------------------------------------------
        edges = cv2.Canny(
            image=image,
            threshold1=50,
            threshold2=150,
            apertureSize=3
        )

        # -------------------------------------------------
        # Detect line segments
        # -------------------------------------------------
        lines = cv2.HoughLinesP(
            image=edges,
            rho=1,
            theta=np.pi / 180,
            threshold=100,
            minLineLength=100,
            maxLineGap=10
        )

        if lines is None:
            return 0.0

        angles = []

        # -------------------------------------------------
        # Compute line angles
        # -------------------------------------------------
        for line in lines:

            x1, y1, x2, y2 = line[0]

            angle = np.degrees(
                np.arctan2(
                    y2 - y1,
                    x2 - x1
                )
            )

            # Keep only near-horizontal lines
            if -45 < angle < 45:
                angles.append(angle)

        if len(angles) == 0:
            return 0.0

        # -------------------------------------------------
        # Robust angle estimation
        # -------------------------------------------------
        estimated_angle = float(np.median(angles))

        return estimated_angle

    def correct(self, image: np.ndarray) -> np.ndarray:
        """
        Correct the skew of a document image.

        Parameters
        ----------
        image : np.ndarray
            Grayscale document image.

        Returns
        -------
        np.ndarray
            Deskewed image.
        """

        # Estimate skew angle
        angle = self.estimate_angle(image)

        print(f"Detected skew angle: {angle:.2f}°")

        # Ignore tiny rotations
        if abs(angle) < 0.1:
            return image

        # -------------------------------------------------
        # Image dimensions
        # -------------------------------------------------
        h, w = image.shape[:2]

        # Center of rotation
        center = (w / 2, h / 2)

        # -------------------------------------------------
        # Rotation matrix
        # -------------------------------------------------
        rotation_matrix = cv2.getRotationMatrix2D(
            center,
            angle,
            1.0
        )

        # -------------------------------------------------
        # Compute new canvas size
        # -------------------------------------------------
        cos = abs(rotation_matrix[0, 0])
        sin = abs(rotation_matrix[0, 1])

        new_width = int((h * sin) + (w * cos))
        new_height = int((h * cos) + (w * sin))

        # -------------------------------------------------
        # Re-center image
        # -------------------------------------------------
        rotation_matrix[0, 2] += (new_width / 2) - center[0]
        rotation_matrix[1, 2] += (new_height / 2) - center[1]

        # -------------------------------------------------
        # Rotate image
        # -------------------------------------------------
        rotated = cv2.warpAffine(
            image,
            rotation_matrix,
            (new_width, new_height),
            flags=cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_CONSTANT,
            borderValue=255
        )

        return rotated