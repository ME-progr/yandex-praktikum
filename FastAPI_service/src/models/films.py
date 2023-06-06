"""Pydantic-схемы для фильмов."""

from models.base import UUIDModel
from models.genres import GenreBase


class FilmPerson(UUIDModel):
    """Класс для представления короткой информации о человеке для фильмов."""

    name: str


class FilmBase(UUIDModel):
    """Класс для представления короткой информации о фильме."""

    title: str
    imdb_rating: float = None


class FilmGenre(UUIDModel):
    """Класс для представления информации о жанрах."""

    name: str


class Film(FilmBase):
    """Класс для представления полной информации о фильме."""

    description: str = None
    genres: list[FilmGenre]
    actors: list[FilmPerson] = []
    writers: list[FilmPerson] = []
    directors: list[FilmPerson] = []
