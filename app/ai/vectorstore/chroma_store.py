from typing import Any

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

    def add(
        self,
        ids: list[str],
        documents: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict[str, Any]],
    ) -> None:
        """
        Store vectors in ChromaDB.
        """
        self._collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def delete(
        self,
        ids: list[str],
    ) -> None:
        """
        Delete vectors by IDs.
        """
        self._collection.delete(ids=ids)

    def count(self) -> int:
        """
        Return total vectors stored.
        """
        return self._collection.count()


# Singleton instance
chroma_store = ChromaStore()