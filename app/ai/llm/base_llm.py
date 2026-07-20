from abc import ABC, abstractmethod


class BaseLLM(ABC):
    """
    Abstract interface for all LLM providers.
    """

    @abstractmethod
    def generate(
        self,
        prompt: str,
        *,
        system_prompt: str | None = None,
    ) -> str:
        """
        Generate a response.

        Args:
            prompt: User prompt.
            system_prompt: Optional system instruction.

        Returns:
            Generated response.
        """
        pass