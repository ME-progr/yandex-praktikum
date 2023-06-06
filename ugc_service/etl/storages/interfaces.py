"""Модуль отвечает за интерфейсы хранилищ."""

from abc import ABC, abstractmethod


class StorageManager(ABC):
    """Менеджер для работы с базой."""
    def __init__(self, client):
        self.client = client

    @abstractmethod
    def on_start_up(self):
        """Действия, которые должны производиться на старте приложения."""

    @abstractmethod
    def on_shut_down(self):
        """Действия, которые должны производиться перед завершением работы приложения."""


class CacheStorage(ABC):
    """Интерфейс для работы с кэш-хранилищами."""

    def __init__(self, client):
        self._client = client

    @abstractmethod
    def get_value(self, key):
        """Метод достает значение по ключу из кэша."""

    @abstractmethod
    def set_value(self, key, value):
        """Метод создаёт пару ключ-значение в кэше."""
