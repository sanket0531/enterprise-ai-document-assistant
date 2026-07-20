from typing import Any

from app.core.logger import get_logger
from app.services.embedding_service import EmbeddingService
from app.ai.vectorstore.vector_service import VectorService

logger = get_logger(__name__)


class RetrieverService:
    """
    Service responsible for semantic document retrieval.

    This service converts a user's query into an embedding,
    searches the vector database, and returns the most
    relevant document chunks.
    """

    def __init__(self) -> None:
        self.embedding_service = EmbeddingService()
        self.vector_service = VectorService()

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        where: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Retrieve the most relevant document chunks.
        """

        logger.info(
            "Searching similar chunks for query: %s",
            query,
        )

        # Generate embedding for the query
        query_embedding = self.embedding_service.generate_embedding(
            query
        )

        # Search ChromaDB
        results = self.vector_service.search_similar_chunks(
            embedding=query_embedding,
            top_k=top_k,
            where=where,
        )

        logger.info(
            "Retrieved %d matching chunks",
            len(results.get("documents", [[]])[0]),
        )

        return results