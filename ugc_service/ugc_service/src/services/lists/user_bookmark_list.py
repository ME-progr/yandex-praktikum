"""Модуль описывает списковые методы для пользовательских отзывов по фильмам"""
from http import HTTPStatus

from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection

from ugc_service.src.core.config import DatabaseName, CollectionName

from .mongo_templates import MongoPageNavigationTemplateList
from .navigation import Navigation
from .sorting import Sorting
from ...models.response_models import UserBookmarkListResponse
from ...models.user_bookmark import UserBookmark


class MongoUserBookmarksList(MongoPageNavigationTemplateList):
    """Класс получает список отзывов по фильму"""

    __slots__ = ('client', 'database', 'collection', 'filter', 'navigation', 'sorting')

    def __init__(
            self,
            client: AsyncIOMotorClient,
            list_filter: dict | None = None,
            navigation: Navigation | None = None,
            sorting: Sorting | None = None,
    ):
        super().__init__(client, list_filter, navigation, sorting)
        self.database: AsyncIOMotorDatabase = self.client[DatabaseName.UGC.value]
        self.collection: AsyncIOMotorCollection = self.database[CollectionName.UserBookmark.value]
        self.model = UserBookmark
        self.response_model = UserBookmarkListResponse

    def _get_query(self) -> dict:
        """Метод получает запрос."""
        try:
            return dict(user_id=self.filter['user_id'])
        except KeyError:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Не задан фильтр по пользователю.')

    def _set_default_sort(self):
        """Метод получает дефолтную сортировку."""
        self.sorting = Sorting()
        self.sorting.append_str_field_sorting('-created_at')
        self.sorting.append_str_field_sorting('-_id')
