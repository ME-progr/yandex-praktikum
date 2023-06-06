"""Модуль описывает интерфейсы обращения к хранилищц данных."""
from abc import ABC, abstractmethod

from models.list_base_models import BaseListResult
from services.lists.navigation import Navigation
from services.lists.sorting import Sorting


class AsyncSearchEngine(ABC):
    """Класс описывает интерфейс общения с поисковым движком."""

    @abstractmethod
    async def get_by_id(self, target: str, uuid: str) -> dict:
        """
        Метод получает данные из поискового движка по ID.

        Args:
            target: источник данных
            uuid: уникальный идентификатор записи.

        Returns:
            данные по ID в виде словаря.
        """

    @abstractmethod
    async def get_list(
            self,
            target: str,
            query: dict | None = None,
            sorting: Sorting | None = None,
            navigation: Navigation | None = None,
    ) -> BaseListResult:
        """
        Метод получает данные из поискового движка в виде списка.

        Args:
            target: источник данных
            query: параметры для запроса.
            sorting: параметры сортировки.
            navigation: параметры навигации.

        Returns:
            BaseListResult
        """
