"""Модуль содержит в себе модели для описания сущности film_review."""
from datetime import datetime

from pydantic import Field

from ugc_service.src.models.base import MongoJSONModel, PyObjectId, DESCRIPTION_FIELD


class FilmReview(MongoJSONModel):
    """Класс описывает модель сущности film_rating."""

    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    film_id: str = Field(...)
    user_id: str = Field(...)
    review: str = DESCRIPTION_FIELD
    created_at: datetime = datetime.now()
