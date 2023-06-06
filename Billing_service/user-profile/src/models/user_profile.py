"""Модуль содержит в себе модели для описания сущностей профиля пользователей."""

import datetime
from typing import Optional

from pydantic import Field

from src.models.base import MongoJSONModel, PyObjectId


class UserProfile(MongoJSONModel):
    """Класс описывает модель сущности user_profile."""

    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    user_id: str = Field(...)
    purchased_films: Optional[list[str]] = Field(default_factory=list)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
