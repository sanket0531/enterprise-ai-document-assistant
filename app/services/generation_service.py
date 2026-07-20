from app.ai.llm.base_llm import BaseLLM
from app.ai.prompts.prompt_builder import PromptBuilder
from app.ai.retrievers.retriever_service import RetrieverService
from app.core.logger import get_logger

logger = get_logger(__name__)


class GenerationService:
    """
    Service responsible for end-to-end RAG answer generation.

    Workflow:
        User Question
            ↓
        Semantic Retrieval
            ↓
        Prompt Builder
            ↓
        LLM Generation
            ↓
        Final Answer
    """

    def __init__(
        self,
        retriever: RetrieverService,
        llm: BaseLLM,
    ) -> None:
        self._retriever = retriever
        self._llm = llm

    def generate_answer(
        self,
        question: str,
        top_k: int = 5,
    ) -> str:
        """
        Generate an answer using the RAG pipeline.

        Args:
            question: User question.
            top_k: Number of chunks to retrieve.

        Returns:
            Generated answer.
        """

        logger.info("Starting RAG answer generation.")

        # Step 1: Retrieve relevant chunks
        retrieval_result = self._retriever.retrieve(
            query=question,
            top_k=top_k,
        )

        logger.info("Retrieved relevant document chunks.")

        # Step 2: Build prompt
        prompt = PromptBuilder.build(
            question=question,
            retrieval_result=retrieval_result,
        )

        logger.info("Prompt built successfully.")

        # Step 3: Generate answer
        answer = self._llm.generate(
            prompt=prompt,
            system_prompt=PromptBuilder.SYSTEM_PROMPT,
        )

        logger.info("Answer generated successfully.")

        return answer