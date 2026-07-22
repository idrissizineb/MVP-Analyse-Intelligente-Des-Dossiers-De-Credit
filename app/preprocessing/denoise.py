import cv2
import numpy as np


class Denoiser:
    """
    Denoise document images before OCR.

    This class provides multiple denoising algorithms that can be
    selected depending on the document type or image quality.

    Supported methods:
        - nlm
        - median
        - gaussian
        - bilateral
    """

    def __init__(
        self,
        method: str = "nlm",
        h: int = 10,
        template_window_size: int = 7,
        search_window_size: int = 21,
        median_kernel: int = 3,
        gaussian_kernel: tuple = (3, 3),
        bilateral_d: int = 9,
        bilateral_sigma_color: int = 75,
        bilateral_sigma_space: int = 75,
    ):
        """
        Initialize the denoiser.

        Parameters
        ----------
        method : str
            Denoising algorithm to use.
            Possible values:
                - "nlm"
                - "median"
                - "gaussian"
                - "bilateral"

        h : int
            Filtering strength for Non-Local Means.

        template_window_size : int
            Template patch size for Non-Local Means.

        search_window_size : int
            Search window size for Non-Local Means.

        median_kernel : int
            Kernel size for Median Blur.
            Must be an odd integer >= 3.

        gaussian_kernel : tuple
            Gaussian kernel size.
            Both values must be positive odd integers.

        bilateral_d : int
            Diameter of the Bilateral Filter.

        bilateral_sigma_color : int
            Color sigma for Bilateral Filter.

        bilateral_sigma_space : int
            Spatial sigma for Bilateral Filter.
        """

        # -------------------------------------------------
        # Supported methods
        # -------------------------------------------------

        supported_methods = {
            "nlm",
            "median",
            "gaussian",
            "bilateral"
        }

        method = method.lower()

        if method not in supported_methods:
            raise ValueError(
                f"Unsupported denoising method '{method}'. "
                f"Supported methods are: {sorted(supported_methods)}"
            )

        # -------------------------------------------------
        # Validate parameters
        # -------------------------------------------------

        if h <= 0:
            raise ValueError("'h' must be greater than zero.")

        if template_window_size <= 0 or template_window_size % 2 == 0:
            raise ValueError(
                "'template_window_size' must be a positive odd integer."
            )

        if search_window_size <= 0 or search_window_size % 2 == 0:
            raise ValueError(
                "'search_window_size' must be a positive odd integer."
            )

        if median_kernel < 3 or median_kernel % 2 == 0:
            raise ValueError(
                "'median_kernel' must be an odd integer >= 3."
            )

        if (
            len(gaussian_kernel) != 2
            or gaussian_kernel[0] <= 0
            or gaussian_kernel[1] <= 0
            or gaussian_kernel[0] % 2 == 0
            or gaussian_kernel[1] % 2 == 0
        ):
            raise ValueError(
                "'gaussian_kernel' must contain two positive odd integers."
            )

        if bilateral_d <= 0:
            raise ValueError(
                "'bilateral_d' must be greater than zero."
            )

        if bilateral_sigma_color <= 0:
            raise ValueError(
                "'bilateral_sigma_color' must be greater than zero."
            )

        if bilateral_sigma_space <= 0:
            raise ValueError(
                "'bilateral_sigma_space' must be greater than zero."
            )

        # -------------------------------------------------
        # Save configuration
        # -------------------------------------------------

        self.method = method

        self.h = h
        self.template_window_size = template_window_size
        self.search_window_size = search_window_size

        self.median_kernel = median_kernel
        self.gaussian_kernel = gaussian_kernel

        self.bilateral_d = bilateral_d
        self.bilateral_sigma_color = bilateral_sigma_color
        self.bilateral_sigma_space = bilateral_sigma_space

    def denoise(self, image: np.ndarray) -> np.ndarray:
        """
        Apply the selected denoising algorithm.

        Parameters
        ----------
        image : np.ndarray
            Grayscale document image.

        Returns
        -------
        np.ndarray
            Denoised image.
        """

        if self.method == "nlm":
            return self._non_local_means(image)


    def _non_local_means(self, image: np.ndarray) -> np.ndarray:
        """
        Apply Fast Non-Local Means denoising.

        Parameters
        ----------
        image : np.ndarray
            Grayscale image.

        Returns
        -------
        np.ndarray
            Denoised image.
        """

        denoised = cv2.fastNlMeansDenoising(
            src=image,
            h=self.h,
            templateWindowSize=self.template_window_size,
            searchWindowSize=self.search_window_size
        )

        return denoised