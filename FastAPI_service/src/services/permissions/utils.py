"""Модуль, содержащий вспомогательные объекты разрешений пользователей."""

from http import HTTPStatus
from jwt import decode, ExpiredSignatureError

from services.permissions.config import RoleName
from core.config import settings


async def get_permission(token: str, allowed_roles: tuple) -> bool:
    """Функция проверяет есть ли необходимая роль у пользователя для разрешения."""

    if token:
        user_roles = await get_user_roles_from_token(token)
    else:
        user_roles = [RoleName.INCOGNITO.value]

    return any(map(lambda user_role: user_role in allowed_roles, user_roles))


async def get_user_roles_from_token(token: str) -> list:
    """Функция взятия списка ролей пользователя из токена."""

    token_data = await decode_token(token)
    return token_data.get('sub', {}).get('user_roles')


async def decode_token(token: str) -> dict:
    """Функция расшифровки токена."""
    options = {
        "verify_signature": False,
        "verify_exp": True
    }
    try:
        return decode(token, algorithms=settings.jwt_algorithm, options=options)
    except ExpiredSignatureError:
        raise ExpiredSignatureError('Срок действия токена истёк.', HTTPStatus.BAD_REQUEST.value)
