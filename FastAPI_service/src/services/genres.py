"""Модуль для представления жанра/ов."""

from functools import lru_cache
from typing import Any

from fastapi import Depends

from core.config import SourceData
from db.elastic import get_elastic
from db.redis import get_redis
from models.genres import GenreBase
from models.list_base_models import GenreListResult
from services.cache.decorators import cache
from .custom_typings import CacheClient, SearchClient
from .lists.navigation import Navigation, NavigationType
from .interfaces import BaseService


class GenreService(BaseService):
    """Класс отвечает за доступные действия с жанрами."""
    source_data = SourceData.ES_GENRES

    @cache(response_model=GenreBase)
    async def get_genre_by_id(self, genre_id: str) -> GenreBase:
        """
        Метод возвращает данные жанра по его ID.

        Args:
            genre_id: UUID жанра.

        Returns:
              GenreBase
        """
        genre = await self.search_engine.get_by_id(self.source_data, genre_id)
        return GenreBase(**genre)

    @cache(response_model=GenreListResult)
    async def get_genres(self, limit: int, search_after: list[Any] | None = None) -> GenreListResult:
        """
        Метод возвращает весь список жанров.

        Args:
            limit: количество записей, которое нужно вернуть.
            search_after: параметр для скроллинга.
            Для получения первой страницы его не нужно передавать, далее передаем то, что вернул ответ функции.
        """
        navigation = Navigation(nav_type=NavigationType.SEARCH_AFTER, limit=limit, search_after=search_after)
        return await self.search_engine.get_list(self.source_data, navigation=navigation)


@lru_cache()
def get_genre_service(
        cache_client: CacheClient = Depends(get_redis),
        search_client: SearchClient = Depends(get_elastic),
) -> GenreService:
    """
    Функция возвращает сервис для работы м жанрами.

    Args:
        redis - клиент Redis.
        elastic - клиент Elasticsearch.

    Returns:
        GenreService
    """
    return GenreService(cache_client, search_client)
