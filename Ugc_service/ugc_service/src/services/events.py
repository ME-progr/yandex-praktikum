"""Модуль для представления Event Service."""

from functools import lru_cache

from fastapi import Depends

from ugc_service.src.db.kafka import get_kafka_producer_client
from ugc_service.src.services.event_storage.factories import get_event_writer_by_client


class EventService:
    """Класс отвечает за доступные действия с хранилищем событий."""

    def __init__(self, event_writer):
        self._event_writer = event_writer

    async def write_event(self, topic: str, key: str, value: str):
        """
        Метод для записи события в хранилище событий.

        Args:
            topic (str): наименование топика для записи.
            key: (str): ключ для записи.
            value: (str): значение для записи.
        """

        await self._event_writer.write_event(topic=topic, key=key, value=value)


@lru_cache()
def get_event_service(
        writer_client=Depends(get_kafka_producer_client),
) -> EventService:
    """
    Функция возвращает сервис для работы с хранилищем событий.

    Args:
        event_writer_service - клиент хранилища событий для записи.

    Returns:
        EventService
    """
    writer = get_event_writer_by_client(writer_client)
    return EventService(writer)
