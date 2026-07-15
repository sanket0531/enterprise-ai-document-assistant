from pathlib import Path

from app.exceptions.extraction import (
    DocumentExtractionException,
    UnsupportedFileTypeException,
)
from app.utils.extractors.docx_extractor import DOCXExtractor
from app.utils.extractors.pdf_extractor import PDFExtractor
from app.utils.extractors.txt_extractor import TXTExtractor


class ExtractionService:
    """
    Service responsible for extracting text from supported document types.
    """

    _extractors = {
        ".pdf": PDFExtractor(),
        ".docx": DOCXExtractor(),
        ".txt": TXTExtractor(),
    }

    @classmethod
    def extract_text(cls, file_path: str) -> str:
        extension = Path(file_path).suffix.lower()

        extractor = cls._extractors.get(extension)

        if extractor is None:
            raise UnsupportedFileTypeException(extension)

        try:
            return extractor.extract(file_path)
        except Exception as exc:
            raise DocumentExtractionException(
                f"Failed to extract text from '{file_path}'."
            ) from exc