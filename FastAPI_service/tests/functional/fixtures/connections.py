"""Модуль содержит в себе фикстуры для установки соединений с различными сервисами."""

import aiohttp
import aioredis
import backoff
import pytest_asyncio
from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import ConnectionError as EsConnectionError

from tests.functional.settings import settings


@backoff.on_exception(backoff.expo, EsConnectionError)
@pytest_asyncio.fixture(scope='session')
async def es_client():
    """Фикстура устанавливает соединение с эластикой на все время активности сессии."""
    client = AsyncElasticsearch(hosts=[f'{settings.elastic_host}:{settings.elastic_port}'])
    yield client
    await client.close()


@backoff.on_exception(backoff.expo, aioredis.RedisError)
@pytest_asyncio.fixture(scope='session')
async def redis_client():
    """Фикстура устанавливает соединение с редисом на все время активности сессии."""
    client = await aioredis.create_redis_pool(
        (settings.redis_host, settings.redis_port),
        minsize=10,
        maxsize=20
    )
    yield client
    client.close()
    await client.wait_closed()


@backoff.on_exception(
    backoff.expo,
    (
        ConnectionRefusedError,
        aiohttp.client.ClientConnectorError,
        aiohttp.client.ClientError,
    ),
)
@pytest_asyncio.fixture(scope='session')
async def api_session():
    """Фикстура инициализирует клиентскую сессию."""
    session = aiohttp.ClientSession(trust_env=True)
    yield session
    await session.close()
