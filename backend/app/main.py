from fastapi import APIRouter, FastAPI

# TODO: import all models here to ensure they are registered with SQLAlchemy

from app.core.config import settings  # NOQA:F401

app = FastAPI(
    title="Dimatech test project API",
)

main_router = APIRouter(prefix="/api", tags=["API"])

# main_router.include_router()  # TODO подключить роутеры

app.include_router(main_router)
