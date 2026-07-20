from __future__ import annotations

import threading

import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    GenerationConfig,
)

from app.ai.llm.base_llm import BaseLLM
from app.ai.llm.exceptions import GenerationError, ModelLoadError
from app.core.logger import get_logger

logger = get_logger(__name__)


class HuggingFaceLLM(BaseLLM):
    """
    Production-ready Hugging Face LLM implementation.

    Features:
    - Lazy model loading
    - Thread-safe initialization
    - GPU/CPU auto detection
    - Chat template support
    - Enterprise logging
    """

    MODEL_NAME = "Qwen/Qwen2.5-3B-Instruct"

    def __init__(self) -> None:
        self._model = None
        self._tokenizer = None
        self._generation_config = None

        self._loaded = False
        self._lock = threading.Lock()

        self._device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )

        logger.info(
            "HuggingFaceLLM initialized. Device: %s",
            self._device,
        )

    def _load_model(self) -> None:
        """
        Lazily load the Hugging Face model and tokenizer.

        The model is loaded only once during the application lifecycle.
        """

        if self._loaded:
            return

        with self._lock:
            if self._loaded:
                return

            try:
                logger.info(
                    "Loading Hugging Face model '%s' on device '%s'...",
                    self.MODEL_NAME,
                    self._device,
                )

                # Load tokenizer
                self._tokenizer = AutoTokenizer.from_pretrained(
                    self.MODEL_NAME,
                    trust_remote_code=True,
                )

                if self._tokenizer.pad_token is None:
                    self._tokenizer.pad_token = self._tokenizer.eos_token

                # Load model
                self._model = AutoModelForCausalLM.from_pretrained(
                    self.MODEL_NAME,
                    torch_dtype=(
                        torch.float16
                        if self._device.type == "cuda"
                        else torch.float32
                    ),
                    trust_remote_code=True,
                    low_cpu_mem_usage=True,
                )

                self._model.to(self._device)
                self._model.eval()

                self._generation_config = GenerationConfig(
                    max_new_tokens=512,
                    temperature=0.3,
                    top_p=0.9,
                    do_sample=True,
                    repetition_penalty=1.1,
                    pad_token_id=self._tokenizer.pad_token_id,
                    eos_token_id=self._tokenizer.eos_token_id,
                )

                self._loaded = True

                logger.info(
                    "Successfully loaded Hugging Face model '%s'.",
                    self.MODEL_NAME,
                )

            except Exception as exc:
                logger.exception("Failed to load Hugging Face model.")

                raise ModelLoadError(
                    f"Unable to load model '{self.MODEL_NAME}'."
                ) from exc

    def generate(
        self,
        prompt: str,
        *,
        system_prompt: str | None = None,
    ) -> str:
        """
        Generate a response from the LLM.

        Args:
            prompt: User prompt.
            system_prompt: Optional system prompt.

        Returns:
            Generated response.

        Raises:
            GenerationError: If generation fails.
        """

        self._load_model()

        try:
            logger.info("Generating response from Hugging Face model.")

            # Build chat messages
            messages = []

            if system_prompt:
                messages.append(
                    {
                        "role": "system",
                        "content": system_prompt,
                    }
                )

            messages.append(
                {
                    "role": "user",
                    "content": prompt,
                }
            )

            # Convert chat to model input
            input_ids = self._tokenizer.apply_chat_template(
                messages,
                tokenize=True,
                add_generation_prompt=True,
                return_tensors="pt",
            )

            input_ids = input_ids.to(self._device)

            # Generate response
            with torch.inference_mode():
                outputs = self._model.generate(
                    input_ids,
                    generation_config=self._generation_config,
                )

            # Remove prompt tokens
            generated_tokens = outputs[0][input_ids.shape[-1]:]

            # Decode response
            response = self._tokenizer.decode(
                generated_tokens,
                skip_special_tokens=True,
            ).strip()

            logger.info("Response generated successfully.")

            return response

        except Exception as exc:
            logger.exception("Generation failed.")

            raise GenerationError(
                "Failed to generate response from the model."
            ) from exc