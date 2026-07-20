from fastapi import APIRouter, Depends

from app.schemas.chat import ChatRequest, ChatResponse
from app.dependencies.dependencies import get_generation_service
from app.services.generation_service import GenerationService

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "",
    response_model=ChatResponse,
)
def chat(
    request: ChatRequest,
    generation_service: GenerationService = Depends(
        get_generation_service
    ),
) -> ChatResponse:
    """
    Chat with uploaded documents.
    """

    answer = generation_service.generate_answer(
        question=request.question,
        top_k=request.top_k,
    )

    return ChatResponse(
        answer=answer,
    )