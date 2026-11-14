
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def test_connection():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
        print("PostgreSQL Connected Successfully!")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
