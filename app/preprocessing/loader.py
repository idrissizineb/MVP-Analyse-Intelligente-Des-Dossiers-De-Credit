#receives the path and determines what kind of file it is
from pathlib import Path

from app.config import SUPPORTED_EXTENSIONS

class DocumentLoader:
    """
    Responsible for validating the input document.

    It DOES NOT read images or convert PDFs.
    It only checks that the file exists and that
    its extension is supported.
    """

    def __init__(self, file_path: str | Path):
        self.file_path= Path(file_path)

    def validate(self) -> None:
        """
        Validate the input document.

        Raises:
            FileNotFoundError
            ValueError when the extension ins't supported
        """

        if not self.file_path.exists():
            raise FileNotFoundError(
                f"File not found: {self.file_path}"
            )

        if self.file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file type: {self.file_path.suffix}"
            )


    def is_pdf(self) -> bool:
        """
        Returns True if the document is a PDF.
        """
        return self.file_path.suffix.lower() == ".pdf"

    def get_path(self) -> Path:
        """
        Returns the validated file path.
        """
        return self.file_path