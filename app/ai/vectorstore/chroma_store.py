from typing import Any
from uuid import UUID

from chromadb.api.models.Collection import Collection

from app.ai.vectorstore.config import chroma_config


class ChromaStore:
    """
    Low-level interface for interacting with ChromaDB.

    This class is responsible only for persistence operations.
    Business logic belongs in VectorService.
    """

    def __init__(self) -> None:
        self._collection: Collection = chroma_config.collection

    def add_embeddings(
        self,
        document_id: UUID,
        chunks: list[str],
        embeddings: list[list[float]],
        metadata: list[dict[str, Any]],
    ) -> None:
        """
        Store document embeddings in ChromaDB.
        """

        ids = [
            f"{document_id}_{index}"
            for index in range(len(chunks))
        ]

        self._collection.add(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadata,
        )

    def search(
        self,
        embedding: list[float],
        top_k: int = 5,
    ):
        """
        Search similar chunks.
        """

        return self._collection.query(
            query_embeddings=[embedding],
            n_results=top_k,
        )

    def delete_document(
        self,
        document_id: UUID,
    ) -> None:
        """
        Delete all vectors belonging to a document.
        """

        self._collection.delete(
            where={
                "document_id": str(document_id)
            }
        )

    def count(self) -> int:
        """
        Return total stored vectors.
        """

        return self._collection.count()

    def peek(self):
        """
        Return sample records from the collection.
        """

        return self._collection.peek()


# Singleton
chroma_store = ChromaStore()