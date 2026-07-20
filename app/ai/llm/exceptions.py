"""
Custom exceptions for the LLM module.
"""


class LLMError(Exception):
    """
    Base exception for all LLM-related errors.
    """

    pass


class ModelLoadError(LLMError):
    """
    Raised when the Hugging Face model fails to load.
    """

    pass


class GenerationError(LLMError):
    """
    Raised when text generation fails.
    """

    pass