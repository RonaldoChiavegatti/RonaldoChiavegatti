from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/agent", tags=["agent"])


class ChatRequest(BaseModel):
    question: str


@router.get("/health")
def health_check():
    return {"status": "ok", "service": "agent"}


@router.post("/chat")
def chat(payload: ChatRequest):
    return {
        "answer": "Ainda vou te responder de verdade 😄 (implementar LLM aqui)",
        "debug": {"question": payload.question},
    }
