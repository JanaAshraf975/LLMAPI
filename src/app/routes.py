
import logging

from fastapi import APIRouter, HTTPException

from app.schema import ChatRequest, ChatResponse
from app.llm import generate_answer

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    logger.info("Chat request received")

    try:
        answer = generate_answer(request.message)
        return ChatResponse(answer=answer)

    except Exception:
        logger.exception("Chat endpoint error")
        raise HTTPException(status_code=500, detail="LLM request failed")


@router.post("/translate", response_model=ChatResponse)
def translate(request: ChatRequest):
    logger.info("Translation request received")

    try:
        answer = generate_answer(
            request.message,
            system_prompt="You are a professional translator. Translate the user's text into English."
        )
        return ChatResponse(answer=answer)

    except Exception:
        logger.exception("Translation endpoint error")
        raise HTTPException(status_code=500, detail="Translation failed")


@router.post("/ask-tourism", response_model=ChatResponse)
def ask_tourism(request: ChatRequest):
    logger.info("Tourism question received")

    try:
        answer = generate_answer(
            request.message,
            system_prompt="You are a tourism expert. Answer questions about tourist destinations, attractions, and travel."
        )
        return ChatResponse(answer=answer)

    except Exception:
        logger.exception("Tourism endpoint error")
        raise HTTPException(status_code=500, detail="Tourism request failed")


@router.post("/travel-plan", response_model=ChatResponse)
def travel_plan(request: ChatRequest):
    logger.info("Travel plan request received")

    try:
        answer = generate_answer(
            request.message,
            system_prompt="You are a travel planner. Create practical travel plans based on the user's preferences, budget, and destination."
        )
        return ChatResponse(answer=answer)

    except Exception:
        logger.exception("Travel plan endpoint error")
        raise HTTPException(status_code=500, detail="Travel planning failed")
