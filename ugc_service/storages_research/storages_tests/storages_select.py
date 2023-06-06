"""Модуль содержит select  запросы для хранилищ."""
from enum import Enum
from clickhouse_driver import Client
from vertica_python import Connection

TClient = Client | Connection


class SelectQuery(Enum):
    """Класс отвечает за названия запросов на выборку данных из хранилища"""

    COUNT = 'Количество записей в таблице.'
    USER_FILMS = 'Фильмы пользователя.'
    FILM_USERS = 'Пользователи фильма.'
    RANDOM_USER = 'Рандомный пользователь'
    RANDOM_FILM = 'Рандомный фильм'


_CLICKHOUSE_QUERIES = {
    SelectQuery.RANDOM_FILM: """SELECT MAX(ugc.film_view.film_id) FROM ugc.film_view""",
    SelectQuery.RANDOM_USER: """SELECT MAX(ugc.film_view.user_id) FROM ugc.film_view""",
    SelectQuery.COUNT: """SELECT COUNT(ugc.film_view.user_id) FROM ugc.film_view""",
    SelectQuery.USER_FILMS: """
        SELECT
            DISTINCT(ugc.film_view.film_id)
        FROM
            ugc.film_view
        WHERE
            ugc.film_view.user_id = {user_id}
    """,
    SelectQuery.FILM_USERS: """
    SELECT
        DISTINCT(ugc.film_view.user_id)
    FROM
        ugc.film_view
    WHERE
        ugc.film_view.film_id = {film_id}
""",
}

_VERTICA_QUERIES = {
    SelectQuery.RANDOM_FILM: """SELECT ugc.film_view.film_id FROM ugc.film_view order by RANDOM() LIMIT 1""",
    SelectQuery.RANDOM_USER: """SELECT ugc.film_view.user_id FROM ugc.film_view order by RANDOM() LIMIT 1""",
    SelectQuery.COUNT: """SELECT COUNT(ugc.film_view.user_id) FROM ugc.film_view""",
    SelectQuery.USER_FILMS: """
        SELECT
            DISTINCT(ugc.film_view.film_id)
        FROM
            ugc.film_view
        WHERE
            ugc.film_view.user_id = {user_id}
    """,
    SelectQuery.FILM_USERS: """
    SELECT
        DISTINCT(ugc.film_view.user_id)
    FROM
        ugc.film_view
    WHERE
        ugc.film_view.film_id = {film_id}
""",
}


def get_select_query_by_client(client: TClient, select_query: SelectQuery) -> str:
    """
    Функция получает запрос по переданному названию и соответствующий заданному клиенту.

    Args:
        client: клиент.
        select_query: запрос, который хотим получить.
    """
    if isinstance(client, Client):
        return _CLICKHOUSE_QUERIES.get(select_query)
    if isinstance(client, Connection):
        return _VERTICA_QUERIES.get(select_query)
