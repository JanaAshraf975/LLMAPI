
from sqlalchemy.orm import Session

from app.models import Request


def create_request(
    db: Session,
    endpoint: str,
    question: str,
    answer: str
):
    new_request = Request(
        endpoint=endpoint,
        question=question,
        answer=answer
    )

    try:
        db.add(new_request)
        db.commit()
        db.refresh(new_request)

        return new_request

    except Exception:
        db.rollback()
        raise
