class UnsupportedFileTypeException(Exception):
    """Raised when an unsupported file type is provided."""

    def __init__(self, extension: str):
        super().__init__(f"Unsupported file type: {extension}")


class DocumentExtractionException(Exception):
    """Raised when document text extraction fails."""

    def __init__(self, message: str):
        super().__init__(message)