import uuid

from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.database import Base


class Request(Base):
    __tablename__ = "requests"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    endpoint = Column(String(100), nullable=False)

    question = Column(Text, nullable=False)

    answer = Column(Text, nullable=False)

    created_at = Column(
        DateTime,
        server_default=func.now(),
        index=True
    )