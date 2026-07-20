from functools import lru_cache

from app.ai.llm.base_llm import BaseLLM
from app.ai.llm.huggingface_llm import HuggingFaceLLM


@lru_cache
def get_llm() -> BaseLLM:
    """
    Returns a singleton LLM instance.

    The instance is cached for the lifetime of the application.
    """
    return HuggingFaceLLM()