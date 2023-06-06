"""Модуль содержит в себе модели для описания сущности film_review."""
from datetime import datetime
from uuid import UUID

from pydantic import Field

from ugc_service.src.models.base import MongoJSONModel, PyObjectId


class UserBookmark(MongoJSONModel):
    """Класс описывает модель сущности film_rating."""

    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    user_id: str = Field(...)
    bookmark_film_id: str | UUID = Field(...)
    created_at: datetime = datetime.now()
