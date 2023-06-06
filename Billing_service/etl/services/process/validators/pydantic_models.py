"""Модуль содержит описание моделей pydantic."""
from pydantic import BaseModel
from etl.services.logs.logs_setup import get_logger

logger = get_logger()


class BillingMovie(BaseModel):
    """Модель, описывающая фильм в биллинге."""

    id: str
    title: str


class Movie(BaseModel):
    """Модель, описывающая фильм в movie."""

    id: str
    subscribe_types: list[str]
