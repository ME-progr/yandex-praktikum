"""Модуль содержит описание базовой раеализации интерфейса севисов."""
from abc import ABC

from services.custom_typings import CacheClient, SearchClient
from services.search_engines.factories import SearchEngineFactory
from .exceptions import MissServiceSourceData


class BaseService(ABC):
    """Базовый тип сервиса."""

    source_data = None

    def __init__(self, cache_client: CacheClient, search_client: SearchClient):
        """
        Инициализирующий метод.

        Args:
            cache_client: клиент кэша
            search_client: клиент источника данных
        """
        if self.source_data is None:
            raise MissServiceSourceData(self)

        self.cache_client = cache_client
        self.search_engine = SearchEngineFactory.get_search_engine_by_client(search_client)
