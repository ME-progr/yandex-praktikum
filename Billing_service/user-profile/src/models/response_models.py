"""Модуль содержит модели, которые могут пригодиться в качестве ответа ручки."""

from src.models.base import JSONModel


class Response(JSONModel):
    """Базовый ответ ручки."""

    detail: str


class IdResponse(JSONModel):
    """Класс описывает тело ответа, содержащее id записи."""

    id: str
