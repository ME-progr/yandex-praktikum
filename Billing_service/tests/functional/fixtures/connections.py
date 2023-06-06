"""Модуль содержит в себе фикстуры для установки соединений с различными сервисами."""

import aiohttp
import backoff
import pytest_asyncio


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
