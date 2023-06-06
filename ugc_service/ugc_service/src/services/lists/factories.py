"""Модуль содержит фабрики для списковых методов."""
from motor.motor_asyncio import AsyncIOMotorClient

from ugc_service.src.services.lists.film_review_list import MongoFilmReviewList
from ugc_service.src.services.lists.interfaces import BaseList
from ugc_service.src.services.lists.navigation import Navigation
from ugc_service.src.services.lists.sorting import Sorting
from ugc_service.src.services.lists.user_bookmark_list import MongoUserBookmarksList
from ugc_service.src.services.types import TStorageClient


_FILM_REVIEWS_LIST = {
    AsyncIOMotorClient: MongoFilmReviewList,
}


_USER_BOOKMARKS_LIST = {
    AsyncIOMotorClient: MongoUserBookmarksList,
}


def get_film_reviews_list_by_client(
    client: TStorageClient,
    list_filter: dict | None,
    navigation: Navigation | None,
    sorting: Sorting | None,
) -> BaseList:
    try:
        cls = _FILM_REVIEWS_LIST[type(client)]
        return cls(client, list_filter, navigation, sorting)
    except KeyError:
        raise KeyError('Не задана реализация для клиента.')


def get_user_bookmarks_list_by_client(
    client: TStorageClient,
    list_filter: dict | None,
    navigation: Navigation | None,
    sorting: Sorting | None,
) -> BaseList:
    try:
        cls = _USER_BOOKMARKS_LIST[type(client)]
        return cls(client, list_filter, navigation, sorting)
    except KeyError:
        raise KeyError('Не задана реализация для клиента.')
