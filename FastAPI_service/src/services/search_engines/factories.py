"""Модуль содержит методы и классы для генерации объектов поисковых движков методов."""

from elasticsearch import AsyncElasticsearch

from .elasticsearch_engine import ESAsyncSearchEngine
from .exceptions import MissSearchEngineRealisation
from .interfaces import AsyncSearchEngine
from ..custom_typings import SearchClient


class SearchEngineFactory:
    """Клас помогает определить конкретную реализацию для спискового метода."""

    @staticmethod
    def get_search_engine_by_client(client: SearchClient, *args, **kwargs) -> AsyncSearchEngine:
        """Метод определяет поисковый движок на основе типа клиента."""
        match client:
            case AsyncElasticsearch():
                return ESAsyncSearchEngine(client)
            case _:
                raise MissSearchEngineRealisation(client)
