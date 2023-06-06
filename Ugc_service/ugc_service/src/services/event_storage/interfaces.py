"""Модуль содержит описание базовой раеализации интерфейса севисов."""

from abc import ABC, abstractmethod


class BaseEventWriter(ABC):
    """Базовый тип сервиса хранилища событий."""

    def __init__(self, event_storage_client):
        """
        Инициализирующий метод.

        Args:
            event_storage_client: клиент хранилища событий
        """

        self._event_storage_client = event_storage_client

    @abstractmethod
    async def write_event(self, topic: str, key: str, value: str):
        """Метод для записи события в хранилище."""
        pass
