"""Модуль содержит модели для тел запросов."""

from src.models.base import JSONModel


class PurchasedFilmRequest(JSONModel):
    """
    Класс описывает модель запроса на добавление/удаление
    купленных фильмов в профиль пользователя.
    """

    user_id: str
    film_ids: list[str]
