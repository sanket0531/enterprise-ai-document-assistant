from chromadb import PersistentClient
from chromadb.api.models.Collection import Collection

from app.core.config import settings


class ChromaConfig:
    """
    ChromaDB configuration and client management.

    Responsible for:
    - Creating a persistent ChromaDB client
    - Creating or retrieving collections
    - Providing shared access to the client and collection
    """

    def __init__(self) -> None:
        self._client = PersistentClient(
            path=settings.chroma_db_path,
        )

    @property
    def client(self) -> PersistentClient:
        """
        Return the shared ChromaDB client.
        """
        return self._client

    @property
    def collection(self) -> Collection:
        """
        Return the configured document collection.
        Creates it automatically if it doesn't exist.
        """
        return self._client.get_or_create_collection(
            name=settings.chroma_collection_name,
        )


# Singleton instance used across the application
chroma_config = ChromaConfig()