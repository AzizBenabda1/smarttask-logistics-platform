from fastapi import APIRouter

from app.schemas.chat_schema import ChatRequest, ChatResponse, ChatSuggestionsResponse
from app.services.chat_service import ChatService

router = APIRouter()
_service = ChatService()


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    return _service.chat(payload)


@router.get("/chat/suggestions", response_model=ChatSuggestionsResponse)
def suggestions(role: str = "MANAGER") -> ChatSuggestionsResponse:
    return _service.get_suggestions(role)
