"""Модуль содержит в себе фикстуры для работы с тестовыми данными."""

import pytest_asyncio
from aiohttp import ClientSession
from aioredis import Redis
from elasticsearch import AsyncElasticsearch

from tests.functional.utils.data_work import cleanup_data_storage, cleanup_cache_storage, user_login
from tests.functional.settings import settings


@pytest_asyncio.fixture(scope='session', autouse=True)
async def data_work(es_client: AsyncElasticsearch, redis_client: Redis):
    """
    Фикстура отвечает за работу с данными в хранилищах
    в начале сессиии и перед завершением сессии.
    Перед завершением сессии происходит
    удаление тестовых данных и кэша из используемых хранилищ.
    """
    yield
    await cleanup_data_storage(es_client)
    await cleanup_cache_storage(redis_client)


@pytest_asyncio.fixture(scope='session', autouse=True)
async def admin_token(
    api_session: ClientSession
):
    """
    Фикстура отвечает за подготовительное получение токенов.
    """

    admin_access_token = await user_login(api_session, settings.admin_login, settings.admin_password)
    yield admin_access_token
