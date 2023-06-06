"""Модуль содержит в себе фикстуры для установки соединений с различными сервисами."""

import aiohttp
import aioredis
import backoff
import pytest_asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ServerSelectionTimeoutError

from settings import settings, mongodb_settings


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


@backoff.on_exception(backoff.expo, ServerSelectionTimeoutError)
@pytest_asyncio.fixture(scope='session')
async def mongodb_client():
    """Фикстура устанавливает соединение с редисом на все время активности сессии."""
    client = AsyncIOMotorClient(
        mongodb_settings.host,
        mongodb_settings.port,
        username=mongodb_settings.username,
        password=mongodb_settings.password,
        serverSelectionTimeoutMS=mongodb_settings.timeout_ms,
    )
    yield client[mongodb_settings.db_name]
    client.close()


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
    session = aiohttp.ClientSession(f'http://{settings.app_host}:{settings.app_port}', trust_env=True)
    yield session
    await session.close()
