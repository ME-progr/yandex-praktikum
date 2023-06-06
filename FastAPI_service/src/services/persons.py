"""Модуль для представления персон."""

from functools import lru_cache
from typing import Any

from fastapi import Depends

from core.config import SourceData
from db.elastic import get_elastic
from db.redis import get_redis
from models.list_base_models import PersonListResult
from models.persons import Person
from services.lists.navigation import Navigation, NavigationType
from services.persons_helpers import adapt_elastic_row_to_person
from .cache.decorators import cache
from .custom_typings import CacheClient, SearchClient
from .interfaces import BaseService


class PersonService(BaseService):
    """Класс отвечает за доступные действия с информацией о людях."""

    source_data = SourceData.ES_PERSONS

    @cache(response_model=Person)
    async def get_person_by_id(self, person_id: str) -> Person:
        """
        Метод возвращает информацию о человеке по `id`, если такой есть.

        Args:
            person_id (str): идентификатор человека

        Returns:
            Person
        """
        person = await self.search_engine.get_by_id(self.source_data, person_id)

        return adapt_elastic_row_to_person(person)

    @cache(response_model=PersonListResult)
    async def get_persons_by_searching(
            self,
            limit: int,
            full_name: str,
            search_after: list[Any] | None = None
    ) -> PersonListResult:
        """
        Метод возвращает список информации о людях соотв. с именем

        Args:
            limit (int): кол-во людей на страницу
            full_name (str): имя человека для поиска
            search_after (list[Any]): отправная точка, от которой идёт следующий поиск

        Returns:
            PersonListResult
        """
        navigation = Navigation(nav_type=NavigationType.SEARCH_AFTER, limit=limit, search_after=search_after)
        query = dict(full_name=full_name) if full_name else None

        return await self.search_engine.get_list(self.source_data, query=query, navigation=navigation)


@lru_cache()
def get_person_service(
        cache_client: CacheClient = Depends(get_redis),
        search_client: SearchClient = Depends(get_elastic),
) -> PersonService:
    """
    Метод возвращает интерфейс для работы с информацией по людям.

    Args:
        cache_client (CacheClient): Кэш-хранилище
        search_client (SearchClient): База данных с людьми

    Returns:
        PersonService
    """
    return PersonService(cache_client, search_client)
