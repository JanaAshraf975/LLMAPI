from fastapi import FastAPI

from .logging_configuration import setup_logging
from .middleware import request_id_middleware
from .routes import router

from .database import Base, engine
from . import models


setup_logging()

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.middleware("http")(request_id_middleware)

app.include_router(router)