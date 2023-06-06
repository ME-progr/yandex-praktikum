"""Модуль для работы с сервисом auth."""
from enum import Enum
from http import HTTPStatus

import requests

from billing.service.errors import MissAuthRoleForSubscribe, ErrorOnRemoteService
from billing.service.remote.utils import validate_remote_settings_with_bearer

from django.conf import settings


class AuthRoleType(str, Enum):
    """Класс описывает роли на сервисе Auth."""

    SUBSCRIBER = 'subscriber'
    AMEDIATEKA = 'amediateka'


def get_role_by_subscribe(subscribe_type: str) -> AuthRoleType:
    """
    Функция получает роль на сервисе auth по значению типа подписки.

    Args:
        subscribe_type: str

    Returns:
        AuthRoleType
    """
    mapping = {
        'SU': AuthRoleType.SUBSCRIBER,
        'AM': AuthRoleType.AMEDIATEKA,
    }

    try:
        return mapping[subscribe_type]
    except KeyError:
        raise MissAuthRoleForSubscribe(f"Отсутствует роль на сервисе auth для подписки {subscribe_type}")


@validate_remote_settings_with_bearer(
    service_name='auth',
    url=settings.AUTH_SERVICE_URL,
    token=settings.AUTH_SERVICE_TOKEN,
)
def add_role_to_user_by_subscribe(user_id, subscribe_type: str) -> bool:
    """
    Функция добавляет роль пользователю на сервис Auth.

    Args:
        user_id: uuid пользователя.
        subscribe_type: наименование подписки в кинотеатре.

    Returns:
        True - роль была добавлена пользователю
        False - роль уже была у пользователя.
    """
    url = f"{settings.AUTH_SERVICE_URL}/auth/api/v1/users/{user_id}/roles/create"

    role = get_role_by_subscribe(subscribe_type)
    response = requests.post(
        url=url,
        headers={
            "Authorization": "Bearer " + settings.AUTH_SERVICE_TOKEN
        },
        json={
            "roles": [f"{role.value}"]
        }
    )

    if response.status_code == HTTPStatus.OK:
        return True
    elif response.status_code == HTTPStatus.CONFLICT:
        return False

    raise ErrorOnRemoteService(f"Ошибка на сервисе auth {response.text}")


@validate_remote_settings_with_bearer(
    service_name='auth',
    url=settings.AUTH_SERVICE_URL,
    token=settings.AUTH_SERVICE_TOKEN,
)
def delete_role_from_user_by_subscribe(user_id, subscribe_type: str):
    role = get_role_by_subscribe(subscribe_type)
    url = f"{settings.AUTH_SERVICE_URL}/auth/api/v1/users/{user_id}/roles/delete?roles={role.value}"

    response = requests.delete(
        url=url,
        headers={
            "Authorization": "Bearer " + settings.AUTH_SERVICE_TOKEN
        },
    )

    if response.status_code != HTTPStatus.OK:
        raise ErrorOnRemoteService(f"Ошибка на сервисе auth {response.text}")
