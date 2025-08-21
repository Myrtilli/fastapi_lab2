from functools import lru_cache
from typing import Annotated
from fastapi import FastAPI
from fastapi.params import Depends
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from src.api import users
from src.middlewares import error_handler
import config
import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
)

@lru_cache
def get_settings():
    return config.Settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Running startup logic before the service starts...")
    # Perform initialization tasks (e.g., database connections, caches)
    yield
    print("Running cleanup logic before shutting down...")

tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users.",
    }
]

app = FastAPI(
    title="Users API",
    description="API for user management",
    version="0.0.1",
    contact={
        "name": "Your Name",
        "email": "your_email@example.com",
    },
)


@app.get("/", tags=["app"])
async def read_root():
    return {"message": "FastAPI is running!"}

@app.get("/info", tags=["app"])
async def info(settings: Annotated[config.Settings,
Depends(get_settings)]):
    return {
    "application_version": settings.APPLICATION_VERSION,
    "test_mode": settings.TEST_MODE
    }

app.include_router(users.router)

app.add_middleware(error_handler.ErrorHandlerMiddleware)
error_handler.setup_exception_handlers(app)

