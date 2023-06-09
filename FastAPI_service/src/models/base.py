"""Базовая Pydantic-схема для классов наследников."""

from uuid import UUID

import orjson
from pydantic import BaseModel


def orjson_dumps(obj, *, default):
    """
    Метод ускоряет работу с JSON

    Args:
        obj (Any): Объект для представления в словарь
        default (Callable): Функция для сериализации.

    Returns: unicode

    """
    return orjson.dumps(obj, default=default).decode()


class UUIDModel(BaseModel):
    """Класс, требующий задать идентификатор всех объектам, унаследованные от `UUIDModel`."""

    id: UUID

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
