"""Pydantic-схемы для жанров."""

from models.base import UUIDModel


class GenreBase(UUIDModel):
    """Класс для представления информации о жанрах."""

    name: str
    description: str = None
