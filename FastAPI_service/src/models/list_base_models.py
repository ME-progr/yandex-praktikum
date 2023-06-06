"""Модуль описывает базовые модели данных, которые могут быть возвращены списочными методами."""

from pydantic import BaseModel

from models.films import FilmBase
from models.genres import GenreBase
from models.persons import Person


class BaseListResult(BaseModel):
    """Базовый результат списочного метода."""

    result: list[BaseModel]
    outcome: dict


class GenreListResult(BaseModel):
    """Результат списочного метода для Жанров."""

    result: list[GenreBase]
    outcome: dict


class FilmListResult(BaseModel):
    """Результат списочного метода для Жанров."""

    result: list[FilmBase]
    outcome: dict


class PersonListResult(BaseModel):
    """Результат списочного метода для Людей."""

    result: list[Person]
    outcome: dict
