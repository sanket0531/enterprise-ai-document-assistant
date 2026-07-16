from app.core.logger import get_logger
from app.utils.chunking import TextChunker

logger = get_logger(__name__)


class ChunkService:
    """
    Service responsible for chunking extracted document text.
    """

    def __init__(self) -> None:
        self._chunker = TextChunker()

    def create_chunks(self, text: str) -> list[str]:
        """
        Convert extracted text into smaller chunks.

        Args:
            text: Extracted document text.

        Returns:
            List of text chunks.
        """
        logger.info("Starting document chunking.")

        chunks = self._chunker.split_text(text)

        logger.info("Document chunking completed. Total chunks: %d", len(chunks))

        return chunks