"""Модуль для представления сервиса для работы с пользовательскими отзывами фильма."""

from functools import lru_cache
from uuid import UUID

from fastapi import Depends

from ugc_service.src.db.mongodb import get_mongo_client
from ugc_service.src.core.config import CollectionName, DatabaseName
from ugc_service.src.db.redis import get_redis
from ugc_service.src.models.film_review import FilmReview
from ugc_service.src.models.response_models import IdResponse, FilmReviewListResponse
from ugc_service.src.services.lists.navigation import Navigation
from ugc_service.src.services.lists.sorting import Sorting
from ugc_service.src.services.lists.factories import get_film_reviews_list_by_client
from ugc_service.src.services.types import TStorageClient, CacheClient
from ugc_service.src.services.crud.factories import get_crud_object_by_client


class FilmUserReviewService:
    """
    Класс отвечает за доступные действия с пользовательскими отзывами на фильмы.

    Attributes:
        cache_client: клиент кэша
        _storage_client: клиент для работы с хранилищем данных.
        _film_user_review: объект для CRUD-операция с хранилищем данных.
    """

    __slots__ = ('cache_client', '_storage_client', '_film_user_review',)

    def __init__(self, storage_client: TStorageClient, cache_client: CacheClient):
        self.cache_client = cache_client
        self._storage_client = storage_client
        self._film_user_review = get_crud_object_by_client(
            storage_client,
            db_name=DatabaseName.UGC.value,
            collection_name=CollectionName.FilmReview.value,
            model=FilmReview,
        )

    async def create_review(self, film_id: UUID | str, user_id: UUID | str, review: str) -> IdResponse:
        """
        Метод устанавливает пользовательский отзыв для фильма.

        Args:
            film_id: иденитфикатор фильма.
            user_id: идентификатор пользователя.
            review: пользовательский отзыв.

        Returns:
            IdResponse
        """
        new_film_review = FilmReview(film_id=film_id, user_id=user_id, review=review)
        created_id = await self._film_user_review.insert(new_film_review)
        return IdResponse(id=created_id)

    async def get_review(self, film_id: UUID | str, user_id: UUID | str) -> FilmReview:
        """
        Метод получает пользовательский отзыв о фильме для конкретного пользователя.

        Args:
            film_id: иденитфикатор фильма.
            user_id: идентификатор пользователя.

        Returns:
            FilmRating
        """
        return await self._film_user_review.get(dict(film_id=film_id, user_id=user_id))

    async def update_review(self, film_id: UUID | str, user_id: UUID | str, review: str) -> FilmReview | None:
        """
        Метод обновляет пользовательский обзор для фильма.

        Args:
            film_id: иденитфикатор фильма.
            user_id: идентификатор пользователя.
            review: пользовательский рейтинг.

        Returns:
            FilmRating
        """
        await self._film_user_review.update(dict(film_id=film_id, user_id=user_id), dict(review=review))
        return await self._film_user_review.get(dict(film_id=film_id, user_id=user_id))

    async def delete_review(self, film_id: UUID | str, user_id: UUID | str):
        """
        Метод удаляет пользовательский рейтинг фильма для конкретного пользователя.

        Args:
            film_id: иденитфикатор фильма.
            user_id: идентификатор пользователя.
        """
        await self._film_user_review.delete(dict(film_id=film_id, user_id=user_id))

    async def get_film_reviews(
            self,
            film_id: UUID | str,
            sort: str,
            limit: int | None,
            page: int | None
    ) -> FilmReviewListResponse:
        """
        Метод реализует поиск списка отзывов к фильму по заданным параметрам.

        Args:
            film_id: идентификатор фильма.
            sort: сортировка (+created_at | -created_at)
            limit: количество записей на странице.
            page: номер страницы.

        Returns:
            FilmReviewListResponse
        """
        sorting = Sorting()
        sorting.append_str_field_sorting(sort)
        navigation = Navigation(limit=limit, page=page) if (limit and page) else None

        film_reviews_list = get_film_reviews_list_by_client(
            self._storage_client,
            dict(film_id=film_id),
            sorting=sorting,
            navigation=navigation,
        )

        return await film_reviews_list.get()


@lru_cache()
def get_film_user_review_service(
        storage_client: TStorageClient = Depends(get_mongo_client),
        cache_client: CacheClient = Depends(get_redis),
) -> FilmUserReviewService:
    """
    Функция возвращает сервис для работы с пользовательским рейтингом фильма.

    Args:
        storage_client: клиент для работы с хранилищем данных.
        cache_client: клиент кэша.

    Returns:
        FilmUserRatingService
    """
    return FilmUserReviewService(storage_client, cache_client)
