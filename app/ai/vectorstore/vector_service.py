from uuid import UUID

from typing import Any
from app.core.logger import get_logger
from app.ai.vectorstore.chroma_store import ChromaStore

logger = get_logger(__name__)


class VectorService:
    """
    Business service responsible for vector database operations.

    This layer hides the underlying vector database implementation
    from the rest of the application.
    """

    def __init__(self) -> None:
        self._store = ChromaStore()

    def store_document_vectors(
        self,
        document_id: UUID,
        chunks: list[str],
        embeddings: list[list[float]],
        metadata: list[dict],
    ) -> None:
        """
        Store document embeddings in the vector database.
        """

        logger.info(
            "Storing %s vectors for document %s",
            len(chunks),
            document_id,
        )

        self._store.add_embeddings(
            document_id=document_id,
            chunks=chunks,
            embeddings=embeddings,
            metadata=metadata,
        )

        logger.info(
            "Successfully stored vectors for document %s",
            document_id,
        )



    def search_similar_chunks(
        self,
        embedding: list[float],
        top_k: int = 5,
        where: dict[str, Any] | None = None,
    ):
        """
        Search similar chunks.
        """

        return self._store.search(
            embedding=embedding,
            top_k=top_k,
            where=where,
        )

    def delete_document_vectors(
        self,
        document_id: UUID,
    ) -> None:
        """
        Delete all vectors belonging to a document.
        """

        logger.info(
            "Deleting vectors for document %s",
            document_id,
        )

        self._store.delete_document(document_id)

    def get_collection_count(self) -> int:
        """
        Return total vectors stored.
        """

        return self._store.count()

