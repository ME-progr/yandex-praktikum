import pymongo
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection

from ugc_service.src.models.base import MongoJSONModel
from ugc_service.src.models.response_models import ListResponse, ListOutcome
from ugc_service.src.services.lists.interfaces import BaseList
from ugc_service.src.services.lists.navigation import Navigation
from ugc_service.src.services.lists.sorting import Sorting
from ugc_service.src.services.lists.utils import adapt_sorting_to_mongo_sort


class MongoPageNavigationTemplateList(BaseList):
    """
    Класс-шаблон для списковых методов постраничной навигации в Mongo.

    Класс не должен использоваться без конкретной реализации.
    """

    def __init__(
            self,
            client: AsyncIOMotorClient,
            list_filter: dict | None = None,
            navigation: Navigation | None = None,
            sorting: Sorting | None = None,
    ):
        super().__init__(list_filter, navigation, sorting)

        self.client = client
        self.database: AsyncIOMotorDatabase = None
        self.collection: AsyncIOMotorCollection = None
        self.result = []
        self.model: type(MongoJSONModel) = None
        self.response_model: type(ListResponse) = None

    async def get(self) -> ListResponse:
        query = self._get_query()
        sorting = self._get_sort()
        cursor = self.collection.find(query)
        cursor = cursor.sort(sorting)

        if self.navigation:
            extra_limit = self.navigation.limit + 1
            cursor.skip(self.navigation.offset).limit(extra_limit)

        async for row in cursor:
            self.result.append(self.model(**row))

        has_more = len(self.result) > self.navigation.limit if self.navigation else False
        next_page = self.navigation.page + 1 if has_more else None

        if self.navigation:
            self.result = self.result[:self.navigation.limit]

        return self.response_model(result=self.result, outcome=ListOutcome(next_page=next_page))

    def _get_sort(self) -> list[tuple[str, pymongo.ASCENDING | pymongo.DESCENDING]]:
        """Метод получает сортировку."""
        if self.sorting:
            if '_id' not in self.sorting.fields_names():
                self.sorting.append_str_field_sorting('-_id')
            return adapt_sorting_to_mongo_sort(self.sorting)

        self._set_default_sort()
        return adapt_sorting_to_mongo_sort(self.sorting)

    async def _get_query(self) -> dict:
        """Метод получает запрос."""
        raise NotImplementedError('Необходимо реализовать собственный метод')

    def _set_default_sort(self):
        """Метод получает запрос."""
        raise NotImplementedError('Необходимо реализовать собственный метод')
