"""Модуль содержит фабрики для поисковиков."""
from functools import lru_cache

from motor.motor_asyncio import AsyncIOMotorClient

from ugc_service.src.services.searchers.searchers import Searcher, MongoAverageRatingSearcher
from ugc_service.src.services.types import TStorageClient


_AVERAGE_RATING_SEARCHERS = {
    AsyncIOMotorClient: MongoAverageRatingSearcher,
}


@lru_cache()
def get_average_rating_searcher_by_client(client: TStorageClient) -> Searcher:
    try:
        cls = _AVERAGE_RATING_SEARCHERS[type(client)]
        return cls(client)
    except KeyError:
        raise KeyError('Не задана реализация для клиента.')
