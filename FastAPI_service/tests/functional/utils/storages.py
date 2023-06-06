"""Объекты для работы с хранилищами."""

from typing import Iterable

import aioredis
import backoff
import orjson
from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import ConnectionError as EsConnectionError
from elasticsearch.helpers import async_bulk, BulkIndexError

from tests.functional.settings import ElasticsearchIndex


@backoff.on_exception(backoff.expo, EsConnectionError)
async def write_data_to_es(
                    es_client: AsyncElasticsearch,
                    es_index: ElasticsearchIndex,
                    data: Iterable[dict]
):
    """Функция отвечает за запись данных в Elasticsearch.

    Args:
        es_client: экземпляр клиента elasticsearch.
        es_index: индекс, в который будут записаны данные.
        data: данные для записи.
    """
    try:
        await async_bulk(es_client, data, index=es_index.value, refresh=True)
    except BulkIndexError:
        raise Exception('Ошибка записи данных в Elasticsearch')


@backoff.on_exception(backoff.expo, aioredis.RedisError)
async def get_item_from_cache(redis_client: Redis, cached_id: str):
    """Функция отвечает за получение объекта из кэша по `cache_id`."""

    result: bytes = await redis_client.get(cached_id)
    if result:
        return orjson.loads(result)
    return {}
