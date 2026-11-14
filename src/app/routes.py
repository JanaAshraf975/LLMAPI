
import logging
import hashlib

from fastapi import APIRouter, HTTPException

from redis.exceptions import RedisError

from app.schema import ChatRequest, ChatResponse
from app.llm import generate_answer
from app.database import SessionLocal
from app.crud import create_request
from app.redis_client import get_cache, set_cache


router = APIRouter()
logger = logging.getLogger(__name__)


def process_request(message, endpoint, system_prompt):

    # Create a unique cache key
    key_data = f"{endpoint}:{message}"
    cache_key = hashlib.sha256(key_data.encode()).hexdigest()

    # Check Redis cache
    try:
        answer = get_cache(cache_key)
    except RedisError:
        logger.warning("Redis cache read failed")
        answer = None

    if answer:
        logger.info("Cache HIT")

    else:
        logger.info("Cache MISS")

        # Generate answer using LLM
        answer = generate_answer(
            message,
            system_prompt=system_prompt
        )

        # Save answer in Redis for 1 hour
        try:
            set_cache(cache_key, answer, ttl=3600)
        except RedisError:
            logger.warning("Redis cache write failed")

    # Connect to PostgreSQL
    db = SessionLocal()

    try:
        # Save question and answer
        create_request(
            db=db,
            endpoint=endpoint,
            question=message,
            answer=answer
        )

    finally:
        db.close()

    return ChatResponse(answer=answer)


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    logger.info("Chat request received")

    try:
        return process_request(
            request.message,
            "chat",
            "You are a helpful assistant."
        )

    except Exception:
        logger.exception("Chat endpoint error")
        raise HTTPException(
            status_code=500,
            detail="Chat request failed"
        )


@router.post("/translate", response_model=ChatResponse)
def translate(request: ChatRequest):

    logger.info("Translation request received")

    try:
        return process_request(
            request.message,
            "translate",
            "You are a professional translator. Translate the user's text into English."
        )

    except Exception:
        logger.exception("Translation endpoint error")
        raise HTTPException(
            status_code=500,
            detail="Translation failed"
        )


@router.post("/ask-tourism", response_model=ChatResponse)
def ask_tourism(request: ChatRequest):

    logger.info("Tourism question received")

    try:
        return process_request(
            request.message,
            "ask-tourism",
            "You are a tourism expert. Answer questions about tourist destinations, attractions, and travel."
        )

    except Exception:
        logger.exception("Tourism endpoint error")
        raise HTTPException(
            status_code=500,
            detail="Tourism request failed"
        )


@router.post("/travel-plan", response_model=ChatResponse)
def travel_plan(request: ChatRequest):

    logger.info("Travel plan request received")

    try:
        return process_request(
            request.message,
            "travel-plan",
            "You are a travel planner. Create practical travel plans based on the user's preferences, budget, and destination."
        )

    except Exception:
        logger.exception("Travel plan endpoint error")
        raise HTTPException(
            status_code=500,
            detail="Travel planning failed"
        )
