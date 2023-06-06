"""Модуль содержит вспомогательные утилиты для тестов."""
from typing import Dict
from uuid import UUID

from storages_research.storages.interfaces import Storage
from storages_research.storages.mongo import MongoStorage
from storages_research.storages_tests.storages_select import (
    SelectQuery,
    get_select_query_by_client,
)


def get_user_id_from_storage(storage: Storage) -> UUID | None:
    sql = get_select_query_by_client(storage.client, SelectQuery.RANDOM_USER)
    result = storage.get_data(sql)
    return result and result[0][0]


def get_film_id_from_storage(storage: Storage) -> UUID | None:
    sql = get_select_query_by_client(storage.client, SelectQuery.RANDOM_FILM)
    result = storage.get_data(sql)
    return result and result[0][0]


def get_mongo_id_pair(storage: MongoStorage) -> Dict:
    row = storage.get_data(query=None)[0]
    return {"film_id": row.get("film_id"), "user_id": row.get("user_id")}
