"""Модуль содержит модели, которые описывают тело HTTP-запроса."""
from uuid import UUID

from pydantic import BaseModel

from ugc_service.src.models.base import RATING_FIELD, DESCRIPTION_FIELD


class RatingBody(BaseModel):
    """Класс описывает тело запроса для установки значения рейтинга."""

    rating: int = RATING_FIELD


class ReviewBody(BaseModel):
    """Класс описывает тело запроса для пользовательского отзыва к фильму."""

    review: str = DESCRIPTION_FIELD


class FilmBookmarkBody(BaseModel):
    """Класс описывает тело запроса для закладок пользователя."""

    bookmark_film_id: UUID | str
