from app.ai.retrievers.retriever_service import RetrieverService
from app.core.logger import get_logger
from app.ai.prompts.prompt_builder import PromptBuilder
logger = get_logger(__name__)


class RAGService:
    """
    Enterprise RAG orchestration service.

    Responsibilities:
    - Retrieve relevant document chunks
    - Build context for the language model
    - Delegate answer generation to an LLM service
    """

    def __init__(self) -> None:
        self._retriever = RetrieverService()
        self._prompt_builder = PromptBuilder()

    def retrieve_context(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[dict]:
        """
        Retrieve relevant chunks for a user query.

        Args:
            query: User question.
            top_k: Number of chunks to retrieve.

        Returns:
            Retrieved chunk metadata.
        """

        logger.info("Retrieving context for RAG pipeline")

        return self._retriever.search(
            query=query,
            top_k=top_k,
        )
    
    def build_prompt(
        self,
        query: str,
        top_k: int = 5,
    ) -> str:
        """
        Retrieve context and build the LLM prompt.
        """

        chunks = self.retrieve_context(
            query=query,
            top_k=top_k,
        )

        return self._prompt_builder.build(
            question=query,
            retrieved_chunks=chunks,
        )

    def answer(
        self,
        query: str,
        top_k: int = 5,
    ) -> str:

        chunks = self.retrieve_context(
            query=query,
            top_k=top_k,
        )

        system_prompt, user_prompt = self._prompt_builder.build(
            question=query,
            retrieved_chunks=chunks,
        )

        return self._llm.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )    