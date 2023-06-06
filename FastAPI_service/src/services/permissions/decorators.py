"""Модуль, содержащий декораторы для сервиса."""

from functools import wraps
from http import HTTPStatus
from jwt import ExpiredSignatureError

from models.exceptions import ExceptionResponse
from services.permissions.config import EndpointAllowedRole
from services.permissions.utils import get_permission


def check_permissions(func):
    """Декоратор проверки доступа пользователя к ручке API."""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        request = kwargs.get('request')

        token = request.headers.get('Authorization')
        if token:
            token = token.split()[-1]

        allowed_roles = EndpointAllowedRole.get_value_by_name(func.__name__.upper())

        try:
            have_permission = await get_permission(token, allowed_roles)
        except ExpiredSignatureError as error:
            return ExceptionResponse(msg=error.args[0], status_code=error.args[1])
        except Exception:
            return ExceptionResponse(
                msg='Что-то пошло не так. Мы уже занимаемся решением проблемы.',
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value
            )

        if not have_permission:
            return ExceptionResponse(msg='Нет разрешения с данной ролью.', status_code=HTTPStatus.FORBIDDEN.value)

        return await func(*args, **kwargs)

    return wrapper
