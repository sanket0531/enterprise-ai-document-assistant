from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """
    Chat request schema.
    """

    question: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="User question",
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Number of chunks to retrieve",
    )


class ChatResponse(BaseModel):
    """
    Chat response schema.
    """

    answer: str