"""Модуль конфигурации для разрешений пользователей."""

from enum import Enum


class ScopeName(Enum):
    """Класс определяющий имена областей разрешения."""

    FILMS = 'films'
    FILM_DETAIL = 'film_details'
    PERSONS = 'persons'
    PERSON_DETAIL = 'person_details'
    GENRES = 'genres'
    PROTECTED = 'protected'


class RoleName(Enum):
    """Класс определяющий имена ролей."""

    ADMIN = 'admin'
    SUBSCRIBER = 'subscriber'
    USER = 'user'
    INCOGNITO = 'incognito'


class EndpointAllowedRole(Enum):
    """Класс определяющий разрешённые роли для конкретных ручек API."""

    SEARCH_FILMS = (
        RoleName.INCOGNITO.value,
        RoleName.USER.value,
        RoleName.SUBSCRIBER.value,
        RoleName.ADMIN.value
    )
    FILM_DETAILS = (
        RoleName.SUBSCRIBER.value,
        RoleName.ADMIN.value
    )
    GET_FILMS = (
        RoleName.INCOGNITO.value,
        RoleName.USER.value,
        RoleName.SUBSCRIBER.value,
        RoleName.ADMIN.value
    )
    GENRE_DETAILS = (
        RoleName.USER.value,
        RoleName.SUBSCRIBER.value,
        RoleName.ADMIN.value
    )
    GENRES = (
        RoleName.INCOGNITO.value,
        RoleName.USER.value,
        RoleName.SUBSCRIBER.value,
        RoleName.ADMIN.value
    )
    SEARCH_PERSONS = (
        RoleName.INCOGNITO.value,
        RoleName.USER.value,
        RoleName.SUBSCRIBER.value,
        RoleName.ADMIN.value
    )
    PERSON_DETAILS = (
        RoleName.USER.value,
        RoleName.SUBSCRIBER.value,
        RoleName.ADMIN.value
    )
    PERSON_FILMS = (
        RoleName.SUBSCRIBER.value,
        RoleName.ADMIN.value
    )

    @classmethod
    def get_value_by_name(cls, name: str) -> tuple:
        for key in cls.__dict__.get('_member_map_').keys():
            if key == name:
                return cls.__dict__.get('_member_map_').get(key).value
