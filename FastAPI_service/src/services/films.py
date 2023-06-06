"""Модуль для представления фильма/ов пользователям."""

from functools import lru_cache
from typing import Any
from uuid import UUID

from fastapi import Depends

from core.config import SourceData
from db.elastic import get_elastic
from db.redis import get_redis
from models.films import Film
from models.list_base_models import FilmListResult
from services.cache.decorators import cache
from services.custom_typings import CacheClient, SearchClient
from services.lists.navigation import Navigation, NavigationType
from services.lists.sorting import Sorting
from .interfaces import BaseService


class FilmService(BaseService):
    """Класс отвечает за доступные действия с фильмами."""

    source_data = SourceData.ES_MOVIES

    @cache(response_model=Film)
    async def get_film_by_id(self, film_id: str) -> Film:
        """
        Метод возвращает фильм, соответствующий уникальному ID, если такой есть.

        Args:
            film_id (str): идентификатор фильма

        Returns:
            Film
        """
        film = await self.search_engine.get_by_id(self.source_data, film_id)

        return Film(**film)

    @cache(response_model=FilmListResult)
    async def get_films(
            self,
            sort: str,
            limit: int,
            search_after: list[Any] | None = None,
            genres: list[UUID] | None = None,
            persons: list[UUID] | None = None,
    ) -> FilmListResult:
        """
        Метод возвращает список фильмов.

        Args:
            sort (str): параметр, по которому будет идти выборка для показа на главной странице
            limit (int): кол-во фильмов на странице
            search_after (list[Any]): отправная точка, от которой идти следующая подборка
            genres (list[UUID]): интересующие жанры для выборки
            persons (list[UUID]): интересующие персоны для выборки

        Returns:
            FilmListResult
        """
        sorting = Sorting()
        sorting.append_str_field_sorting(sort)

        navigation = Navigation(nav_type=NavigationType.SEARCH_AFTER, limit=limit, search_after=search_after)

        query = {}
        if genres:
            query.update(dict(genres=genres))
        if persons:
            query.update(dict(persons=persons))

        return await self.search_engine.get_list(self.source_data, query, sorting, navigation)

    @cache(response_model=FilmListResult)
    async def get_films_by_searching(
            self,
            limit: int,
            title: str,
            search_after: list[Any] | None = None
    ) -> FilmListResult:
        """
        Метод возвращает список фильмов соотв. с названием

        Args:
            limit (int): кол-во фильмов на страницу
            title (str): название фильма для поиска
            search_after (list[Any]): отправная точка, от которой идёт следующий поиск

        Returns:
            FilmListResult
        """
        navigation = Navigation(nav_type=NavigationType.SEARCH_AFTER, limit=limit, search_after=search_after)

        query = dict(title=title) if title else None

        return await self.search_engine.get_list(self.source_data, query, navigation=navigation)


@lru_cache
def get_film_service(
        cache_client: CacheClient = Depends(get_redis),
        search_client: SearchClient = Depends(get_elastic),
) -> FilmService:
    """
    Метод возвращает интерфейс для работы с фильмами

    Args:
        cache_client (CacheClient): Кэш-хранилище
        search_client (SearchClient): База данных с фильмами

    Returns:
        FilmService
    """
    return FilmService(cache_client, search_client)
