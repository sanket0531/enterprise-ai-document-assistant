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
    def generate_embedding(
        text: str,
    ) -> list[float]:
        """
        Generate an embedding for a single text.

        Args:
            text: Input text.

        Returns:
            Embedding vector.
        """

        if not text.strip():
            logger.warning("Empty text provided for embedding generation.")
            return []

        logger.info("Generating embedding for query.")

        try:
            embedding = EmbeddingUtility.generate_embeddings([text])[0]

            logger.info("Successfully generated query embedding.")

            return embedding

        except Exception as exc:
            logger.exception(
                "Query embedding generation failed."
            )

            raise EmbeddingGenerationException(
                "Failed to generate query embedding."
            ) from exc