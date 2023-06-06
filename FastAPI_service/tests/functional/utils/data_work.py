"""Модуль содержит в себе функции, реализующие работу с тестовыми данными."""

from aiohttp import ClientSession
from elasticsearch import AsyncElasticsearch
from aioredis import Redis

from tests.functional.settings import settings
from tests.functional.utils.api import api_request


async def cleanup_data_storage(storage_client: AsyncElasticsearch):
    """
    Очистка тестового хранилища данных один раз по окончанию сессии.

    Args:
        storage_client: экземпляр клиента хранилища данных.
    """
    await storage_client.delete_by_query(index='_all',
                                         body={"query": {"match_all": {}}},
                                         refresh=True)


async def cleanup_cache_storage(cache_client: Redis):
    """
    Очистка тестового хранилища кэша один раз по окончанию сессии.

    Args:
        cache_client: экземпляр клиента хранилища кэша.
    """
    await cache_client.flushdb(async_op=True)


async def user_login(
        api_session: ClientSession,
        login: str,
        pwd: str
) -> tuple[str, str]:
    """
    Функция реализующая вход в систему пользователя.

    Args:
        api_session: экзепляр клиентской сессии.
        login: логин пользователя.
        pwd: пароль пользователя.

    Returns:
        кортеж токенов.
    """
    query = {
        "login": login,
        "password": pwd
    }
    url = f'{settings.auth_service_url}/auth/api/v1/account/login'
    body, headers, status = await api_request(api_session, 'post', url, json=query)
    return body.get('access_token')
