"""Модуль отвечает за интерфейсы хранилищ."""
from abc import ABC, abstractmethod
from typing import Iterable


class Storage(ABC):
    """Интерфейс хранилища."""

    name = 'storage'

    def __init__(self, client):
        self.client = client

    @abstractmethod
    def get_data(self, query: str, chunk_size: int | None = None):
        """
        Метод отвечает за получение данных по запросу.

        Args:
            query: запрос для получения данных.
            chunk_size: размер чанка данных, в которых будем получать данные.
        """
        pass

    @abstractmethod
    def write_data(self, target: str, data: Iterable[dict | tuple]):
        """
        Метод отвечает за запись данных в целевой объект.

        Args:
            target: целевой объект.
            data: данные.
        """
        pass

    @abstractmethod
    def import_from_csv(self, target: str, file_path: str, converters: dict):
        """
        Метод отвечает за импортирование данных из csv файла в целевую таблицу.

        Args:
            target: целевая таблица.
            file_path: путь до файла.
            converters: конвертеры для полей csv файла. Пример dict(user_id=int)
        """
        pass


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