"""Модуль содержит различные поисковики специализированной информации по пользовательскому рейтингу фильмов."""
from abc import ABC
from http import HTTPStatus
from typing import Any
from uuid import UUID

from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection

from ugc_service.src.core.config import DatabaseName, CollectionName
from ugc_service.src.models.film_rating import AverageRating


class Searcher(ABC):
    """Базовый интерфей для поиска"""

    async def get(self, *args, **kwargs) -> Any:
        """
        Метод осуществляет поиск информации в зависимости от конкретной реализации.

        Args:
            args: позиционные параметры.
            kwargs: именнованые параметры.

        Returns:
            Any
        """
        raise NotImplementedError('Необходимо реализовать метод интерфейса!')


class MongoAverageRatingSearcher(Searcher):
    """Класс отвечает за поиск среднего рейтинга фильма в MongoDB"""

    def __init__(self, client: AsyncIOMotorClient):
        self._client = client
        self._database: AsyncIOMotorDatabase = self._client[DatabaseName.UGC.value]
        self._collection: AsyncIOMotorCollection = self._database[CollectionName.FilmRating.value]

    async def get(self, film_id: UUID | str) -> AverageRating:
        """
        Метод осуществляет поиск среднего пользовательского рейтинга фильма.

        Args:
            film_id: идентификатор фильма.

        Returns:
            float
        """
        pipeline = [
            {
                '$match': {'film_id': film_id}
            },
            {
                '$group': {
                    '_id': '$film_id',
                    'average_rating': {'$avg': '$rating'}
                }
            },
        ]

        cursor = self._collection.aggregate(pipeline)
        average_ratings = await cursor.to_list(length=1)

        try:
            average_rating = average_ratings[0]
            return AverageRating(film_id=average_rating.get('_id'), average_rating=average_rating.get('average_rating'))
        except IndexError:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Такого фильма не существует!")
