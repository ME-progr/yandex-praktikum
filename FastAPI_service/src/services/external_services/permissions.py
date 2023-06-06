"""Модуль, содержащий вспомогательные объекты."""

import aiohttp

from .utils import api_request
from src.models.exceptions import ExceptionResponse
from src.models.permissions import PermissionsResponse


async def get_user_permissions(
        api_session: aiohttp.ClientSession,
        scope: str,
        token: str = None
) -> PermissionsResponse | ExceptionResponse:
    """
    Функция создаёт запрос на разрешения пользователя по области разрешения и токену.
    Если токена нет, то возвращаются разрешения по роли `incognito`.
    """

    url = '/auth/api/v1/user-permissions'
    query = {'scope': scope}

    response = await api_request(
        api_session,
        'GET',
        url,
        params=query,
        token=token
    )
    if isinstance(response, ExceptionResponse):
        return response

    return PermissionsResponse(**response.get('body'))
