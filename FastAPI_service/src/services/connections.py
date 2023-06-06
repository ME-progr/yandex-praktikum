"""Модуль, содержащий объекты различных соединений."""

from functools import lru_cache

import aiohttp
import backoff
from starlette.requests import Request


@lru_cache()
@backoff.on_exception(
    backoff.expo,
    (
        ConnectionRefusedError,
        aiohttp.client.ClientConnectorError,
        aiohttp.client.ClientError,
    ),
)
def api_session(request: Request) -> aiohttp.ClientSession:
    """Функция инициализирует клиентскую сессию."""

    return request.app.state.api_session
