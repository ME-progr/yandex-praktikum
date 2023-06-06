"""Модуль содержит модели, которые могут пригодиться в качестве ответа ручки."""

from pydantic import BaseModel

from ugc_service.src.models.base import MongoJSONModel
from ugc_service.src.models.film_review import FilmReview
from ugc_service.src.models.user_bookmark import UserBookmark


class Response(BaseModel):
    """Базовый ответ ручки."""

    detail: str


class IdResponse(BaseModel):
    """Класс описывает тело ответа, содержащее id записи."""

    id: str


class ListOutcome(MongoJSONModel):
    """Класс описывает outcome для списковых методов."""

    next_page: int | None = None


class ListResponse(MongoJSONModel):
    """Класс описывает стандартный ответ для списковых методов"""

    result: list[BaseModel]
    outcome: ListOutcome


class FilmReviewListResponse(MongoJSONModel):
    """Класс описывает ответ для спискового метода отзывов по фильму"""

    result: list[FilmReview]
    outcome: ListOutcome


class UserBookmarkListResponse(MongoJSONModel):
    """"Класс описывает ответ для спискового метода пользовательских закладок по фильмам."""

    result: list[UserBookmark]
    outcome: ListOutcome
