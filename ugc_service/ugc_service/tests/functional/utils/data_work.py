"""Модуль содержит в себе функции, реализующие работу с тестовыми данными."""

from aioredis import Redis


async def cleanup_cache_storage(cache_client: Redis):
    """
    Очистка тестового хранилища кэша один раз по окончанию сессии.

    Args:
        cache_client: экземпляр клиента хранилища кэша.
    """
    await cache_client.flushdb(async_op=True)
