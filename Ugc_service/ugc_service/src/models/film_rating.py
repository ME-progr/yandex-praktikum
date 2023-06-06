"""Модуль содержит в себе модели для описания сущности film_rating."""

from pydantic import Field, BaseModel

from ugc_service.src.models.base import MongoJSONModel, PyObjectId, RATING_FIELD


class FilmRating(MongoJSONModel):
    """Класс описывает модель сущности film_rating."""

    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    film_id: str = Field(...)
    user_id: str = Field(...)
    rating: int = RATING_FIELD


class AverageRating(BaseModel):
    """Класс описывает средний пользовательский рейтинг."""

    film_id: str
    average_rating: float = RATING_FIELD
