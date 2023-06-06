"""Модуль для представления сервиса для работы с пользовательскими закладками"""

from functools import lru_cache
from uuid import UUID

from fastapi import Depends

from ugc_service.src.db.mongodb import get_mongo_client
from ugc_service.src.core.config import CollectionName, DatabaseName
from ugc_service.src.db.redis import get_redis
from ugc_service.src.models.response_models import IdResponse, UserBookmarkListResponse
from ugc_service.src.models.user_bookmark import UserBookmark
from ugc_service.src.services.lists.navigation import Navigation
from ugc_service.src.services.lists.sorting import Sorting
from ugc_service.src.services.lists.factories import get_user_bookmarks_list_by_client
from ugc_service.src.services.types import TStorageClient, CacheClient
from ugc_service.src.services.crud.factories import get_crud_object_by_client


class UserBookmarkService:
    """
    Класс отвечает за доступные действия с пользовательскими закладками.

    Attributes:
        cache_client: клиент кэша
        _storage_client: клиент для работы с хранилищем данных.
        _film_user_review: объект для CRUD-операция с хранилищем данных.
    """

    __slots__ = ('cache_client', '_storage_client', '_user_bookmark_service',)

    def __init__(self, storage_client: TStorageClient, cache_client: CacheClient):
        self.cache_client = cache_client
        self._storage_client = storage_client
        self._user_bookmark_service = get_crud_object_by_client(
            storage_client,
            db_name=DatabaseName.UGC.value,
            collection_name=CollectionName.UserBookmark.value,
            model=UserBookmark,
        )

    async def add_film_to_user_bookmarks(self, film_id: UUID | str, user_id: UUID | str) -> IdResponse:
        """
        Метод добавляет фильм в пользовательские закладки.

        Args:
            film_id: иденитфикатор фильма.
            user_id: идентификатор пользователя.

        Returns:
            IdResponse
        """
        new_user_bookmark = UserBookmark(bookmark_film_id=film_id, user_id=user_id)
        created_id = await self._user_bookmark_service.insert(new_user_bookmark)
        return IdResponse(id=created_id)

    async def delete_film_from_user_bookmarks(self, film_id: UUID | str, user_id: UUID | str):
        """
        Метод удаляет пользовательский рейтинг фильма для конкретного пользователя.

        Args:
            film_id: иденитфикатор фильма.
            user_id: идентификатор пользователя.
        """
        await self._user_bookmark_service.delete(dict(bookmark_film_id=film_id, user_id=user_id))

    async def get_user_bookmarks(
        self,
        user_id: UUID | str,
        sort: str,
        limit: int | None,
        page: int | None,
    ) -> UserBookmarkListResponse:
        """
        Метод реализует поиск пользовательских закладок.

        Args:
            user_id: идентификатор пользователя.
            sort: сортировка (+created_at | -created_at)
            limit: количество записей на странице.
            page: номер страницы.

        Returns:
            UserBookmarkListResponse
        """
        sorting = Sorting()
        sorting.append_str_field_sorting(sort)
        navigation = Navigation(limit=limit, page=page) if (limit and page) else None

        user_bookmark_list = get_user_bookmarks_list_by_client(
            self._storage_client,
            dict(user_id=user_id),
            sorting=sorting,
            navigation=navigation,
        )

        return await user_bookmark_list.get()


@lru_cache()
def get_user_bookmark_service(
        storage_client: TStorageClient = Depends(get_mongo_client),
        cache_client: CacheClient = Depends(get_redis),
) -> UserBookmarkService:
    """
    Функция возвращает сервис для работы с пользовательскими закладками.

    Args:
        storage_client: клиент для работы с хранилищем данных.
        cache_client: клиент кэша.

    Returns:
        UserBookmarkService
    """
    return UserBookmarkService(storage_client, cache_client)
