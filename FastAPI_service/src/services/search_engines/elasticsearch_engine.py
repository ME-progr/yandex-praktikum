"""Модуль отвечает за описание поискового движка Elasticsearch."""
from http import HTTPStatus

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import HTTPException
from pydantic import BaseModel

from core.config import SourceData
from models.list_base_models import BaseListResult
from services.lists.factories import ListFactory
from services.lists.navigation import Navigation
from services.lists.sorting import Sorting
from .interfaces import AsyncSearchEngine


class ESAsyncSearchEngine(AsyncSearchEngine):
    """Класс предоставляет интерфейс для работы с поисковым движком для Elasticsearch."""

    def __init__(self, client: AsyncElasticsearch):
        """
        Инициализирующий метод.

        Args:
            client: асинхронный клиент эластики.
        """
        self._client = client

    async def get_by_id(self, target: SourceData, uuid: str) -> BaseModel:
        """
        Метод получает данные из поискового движка по ID.

        Args:
            target: источник данных
            uuid: уникальный идентификатор записи.

        Returns:
            данные по ID в виде словаря.
        """
        try:
            doc = await self._client.get(target.value, uuid)
        except NotFoundError:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'Для {target} не найдены данные по id: {uuid}',
            )
        return doc['_source']

    async def get_list(
            self,
            target: SourceData,
            query: dict | None = None,
            sorting: Sorting | None = None,
            navigation: Navigation | None = None,
    ) -> BaseListResult:
        """
        Метод получает данные из поискового движка в виде списка.

        Args:
            target: источник данных
            query: параметры для запроса.
            sorting: параметры сортировки.
            navigation: параметры навигации.

        Returns:
            BaseListResult
        """
        params = dict(query=query, sorting=sorting, navigation=navigation)
        searcher = ListFactory.get_list_searcher_by_target(target, self._client, **params)
        return await searcher.get()
