"""Модуль для представления сервиса для работы с пользовательским рейтингом фильма."""

from functools import lru_cache
from uuid import UUID

from fastapi import Depends

from ugc_service.src.db.mongodb import get_mongo_client
from ugc_service.src.core.config import CollectionName, DatabaseName
from ugc_service.src.db.redis import get_redis
from ugc_service.src.models.film_rating import FilmRating, AverageRating
from ugc_service.src.models.response_models import IdResponse
from ugc_service.src.services.cache.decorators import cache
from ugc_service.src.services.types import TStorageClient, CacheClient
from ugc_service.src.services.crud.factories import get_crud_object_by_client
from ugc_service.src.services.searchers.factories import get_average_rating_searcher_by_client


class FilmUserRatingService:
    """
    Класс отвечает за доступные действия с пользовательским рейтингом фильмов.

    Attributes:
        cache_client: клиент кэша
        _storage_client: клиент для работы с хранилищем данных.
        _film_user_rating: объект для CRUD-операция с хранилищем данных.
        _average_rating_searcher: поисковик среднего рейтинга.
    """

    __slots__ = ('cache_client', '_storage_client', '_film_user_rating', '_average_rating_searcher')

    def __init__(self, storage_client: TStorageClient, cache_client: CacheClient):
        self.cache_client = cache_client
        self._storage_client = storage_client
        self._film_user_rating = get_crud_object_by_client(
            storage_client,
            db_name=DatabaseName.UGC.value,
            collection_name=CollectionName.FilmRating.value,
            model=FilmRating,
        )
        self._average_rating_searcher = get_average_rating_searcher_by_client(storage_client)

    async def set_rating(self, film_id: UUID | str, user_id: UUID | str, rating: int) -> IdResponse:
        """
        Метод устанавливает пользовательский рейтинг для фильма.

        Args:
            film_id: иденитфикатор фильма.
            user_id: идентификатор пользователя.
            rating: пользовательский рейтинг.

        Returns:
            IdResponse
        """
        new_film_rating = FilmRating(film_id=film_id, user_id=user_id, rating=rating)
        created_id = await self._film_user_rating.insert(new_film_rating)
        return IdResponse(id=created_id)

    @cache(response_model=FilmRating)
    async def get_rating(self, film_id: UUID | str, user_id: UUID | str) -> FilmRating:
        """
        Метод получает пользовательский рейтинг фильма для конкретного пользователя.

        Args:
            film_id: иденитфикатор фильма.
            user_id: идентификатор пользователя.

        Returns:
            FilmRating
        """
        return await self._film_user_rating.get(dict(film_id=film_id, user_id=user_id))

    async def update_rating(self, film_id: UUID | str, user_id: UUID | str, rating: int) -> FilmRating | None:
        """
        Метод устанавливает пользовательский рейтинг для фильма.

        Args:
            film_id: иденитфикатор фильма.
            user_id: идентификатор пользователя.
            rating: пользовательский рейтинг.

        Returns:
            FilmRating
        """
        await self._film_user_rating.update(dict(film_id=film_id, user_id=user_id), dict(rating=rating))
        return await self._film_user_rating.get(dict(film_id=film_id, user_id=user_id))

    async def delete_rating(self, film_id: UUID | str, user_id: UUID | str):
        """
        Метод удаляет пользовательский рейтинг фильма для конкретного пользователя.

        Args:
            film_id: иденитфикатор фильма.
            user_id: идентификатор пользователя.
        """
        await self._film_user_rating.delete(dict(film_id=film_id, user_id=user_id))

    async def get_average_rating(self, film_id: UUID | str) -> AverageRating:
        """
        Метод получает средний пользовательский рейтинг указанного фильма

        Args:
            film_id: идентификатор фильма.

        Returns:
            AverageRating.
        """
        return await self._average_rating_searcher.get(film_id)


@lru_cache()
def get_film_user_rating_service(
        storage_client: TStorageClient = Depends(get_mongo_client),
        cache_client: CacheClient = Depends(get_redis),
) -> FilmUserRatingService:
    """
    Функция возвращает сервис для работы с пользовательским рейтингом фильма.

    Args:
        storage_client: клиент для работы с хранилищем данных.
        cache_client: клиент кэша.

    Returns:
        FilmUserRatingService
    """
    return FilmUserRatingService(storage_client, cache_client)
