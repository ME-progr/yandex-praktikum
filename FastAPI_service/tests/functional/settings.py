"""Модуль содержит настройки для тестов."""
import os.path
from enum import Enum
from pathlib import Path

from pydantic import BaseSettings, Field

BASE_DIR = Path(__file__).resolve().parent


class ElasticsearchIndex(Enum):
    """Класс описывает названия индексов"""
    MOVIES = 'movies'
    GENRES = 'genres'
    PERSONS = 'persons'


class NamesOfClasses(str, Enum):
    """Класс описывает наименования всех `Service`-классов, используемые в API."""

    MOVIES = 'FilmService'
    GENRES = 'GenreService'
    PERSONS = 'PersonService'


class NamesOfFunctions(str, Enum):
    """Класс описывает наименования всех функций `Service`-классов, используемые в API."""

    MOVIE_ID = 'get_film_by_id'
    LIST_MOVIES = 'get_films'
    SEARCH_MOVIES = 'get_films_by_searching'
    GENRE_ID = 'get_genre_by_id'
    LIST_GENRES = 'get_genres'
    PERSON_ID = 'get_person_by_id'
    SEARCH_PERSONS = 'get_persons_by_searching'


class Settings(BaseSettings):
    """Класс описывает базовые нстройки для тестов."""

    service_url: str = Field(..., env='SERVICE_URL')
    auth_service_url: str = Field(..., env='AUTH_SERVICE_URL')

    redis_host: str = Field(..., env='REDIS_HOST')
    redis_port: int = Field(..., env='REDIS_PORT')

    elastic_host: str = Field(..., env='ELASTIC_HOST')
    elastic_port: int = Field(..., env='ELASTIC_PORT')

    elastic_index: type(ElasticsearchIndex) = ElasticsearchIndex

    cache_live_seconds: int = Field(..., env='CACHE_LIVE_SECONDS')
    cls_names_for_cached_id: type(NamesOfClasses) = NamesOfClasses
    foo_names_for_cached_id: type(NamesOfFunctions) = NamesOfFunctions

    admin_login: str = Field(..., env='ADMIN_LOGIN')
    admin_password: str = Field(..., env='ADMIN_PASSWORD')

    class Config:
        env_file = os.path.join(BASE_DIR, '.env.prod')


settings = Settings()
