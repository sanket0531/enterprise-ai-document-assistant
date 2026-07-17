from app.core.logger import get_logger

from sentence_transformers import SentenceTransformer

from app.core.config import settings

logger = get_logger(__name__)


class EmbeddingUtility:
    """
    Utility class responsible for generating text embeddings
    using a Hugging Face SentenceTransformer model.
    """

    _model: SentenceTransformer | None = None

    @classmethod
    def get_model(cls) -> SentenceTransformer:
        """
        Lazily load the embedding model.
        The model is loaded only once and reused.
        """

        if cls._model is None:
            logger.info(
                "Loading embedding model: %s",
                settings.embedding_model,
            )

            cls._model = SentenceTransformer(
                settings.embedding_model
            )

            logger.info("Embedding model loaded successfully.")

        return cls._model

    @classmethod
    def generate_embeddings(
        cls,
        texts: list[str],
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple texts.

        Args:
            texts: List of input strings.

        Returns:
            List of embedding vectors.
        """

        model = cls.get_model()

        embeddings = model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=False,
        )
        return embeddings.tolist()