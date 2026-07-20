from functools import lru_cache

from app.ai.llm.dependencies import get_llm
from app.ai.retrievers.retriever_service import RetrieverService
from app.services.generation_service import GenerationService


@lru_cache
def get_retriever() -> RetrieverService:
    return RetrieverService()


@lru_cache
def get_generation_service() -> GenerationService:
    return GenerationService(
        retriever=get_retriever(),
        llm=get_llm(),
    )