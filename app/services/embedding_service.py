from app.core.logger import get_logger

from app.utils.embedding import EmbeddingUtility
from app.exceptions.embedding import (
    EmbeddingGenerationException,
)

logger = get_logger(__name__)

class EmbeddingService:
    """
    Service responsible for generating embeddings
    for document chunks.
    """

    @staticmethod
    def generate_embeddings(
        chunks: list[str],
    ) -> list[list[float]]:
        """
        Generate embeddings for document chunks.

        Args:
            chunks: List of text chunks.

        Returns:
            List of embedding vectors.
        """

        if not chunks:
            logger.warning("No chunks provided for embedding generation.")
            return []

        logger.info(
            "Generating embeddings for %d chunks.",
            len(chunks),
        )

        try:
            embeddings = EmbeddingUtility.generate_embeddings(
                chunks
            )

            logger.info(
                "Successfully generated %d embeddings.",
                len(embeddings),
            )

            return embeddings

        except Exception as exc:
            logger.exception(
                "Embedding generation failed."
            )

            raise EmbeddingGenerationException(
                "Failed to generate embeddings."
            ) from exc