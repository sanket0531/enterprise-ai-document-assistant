from abc import ABC, abstractmethod


class BaseExtractor(ABC):
    """
    Abstract base class for all document extractors.
    """

    @abstractmethod
    def extract(self, file_path: str) -> str:
        """
        Extract text from a document.

        Args:
            file_path: Absolute path to the document.

        Returns:
            Extracted document text.
        """
        pass