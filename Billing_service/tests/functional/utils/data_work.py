"""Модуль содержит в себе функции, реализующие работу с тестовыми данными."""

from aiohttp.client import ClientSession

from tests.functional.utils.api import api_request
from tests.functional.settings import settings


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
    url = f'http://{settings.auth_host}:{settings.auth_port}/auth/api/v1/account/login'
    body, headers, status = await api_request(api_session, 'POST', url, json=query)
    return body.get('access_token'), body.get('refresh_token')


async def signup_user(
        api_session: ClientSession,
        login: str,
        email: str,
        pwd: str
):
    """
    Функция реализующая регистрацию пользователя.

    Args:
        api_session: экзепляр клиентской сессии.
        login: логин пользователя.
        email: e-mail пользователя.
        pwd: пароль пользователя.
    """
    query = {
        "login": login,
        "email": email,
        "password": pwd
    }
    url = f'http://{settings.auth_host}:{settings.auth_port}/auth/api/v1/account/signup'
    await api_request(api_session, 'POST', url, json=query)
