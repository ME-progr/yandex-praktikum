"""Модуль содержит базовый интерфейс для всех списочных методов, которые могут пригодиться в API."""

from abc import ABC, abstractmethod

from models.list_base_models import BaseListResult
from services.custom_typings import SearchClient
from services.lists.navigation import Navigation
from services.lists.sorting import Sorting


class BaseList(ABC):
    """Класс описывает интерфейс для всех списочных методов, извлекающих данные из Elasticsearch."""

    def __init__(
            self,
            search_client: SearchClient,
            query: dict | None = None,
            sorting: Sorting | None = None,
            navigation: Navigation | None = None
    ):
        """
        Инициализирующий метод.

        Args:
            search_client: клиент базы данных, на основе которого будет производиться поиск.
            query: различные параметры фильтрации, которые должны быть обработаны.
            sorting: Сортировка различных полей. Не обязательный параметр.
            navigation: Навигация по результатам. Не ообязательный параметр.
        """
        self._search_client = search_client
        self._query = query
        self._sorting = sorting
        self._navigation = navigation

    @abstractmethod
    async def get(self) -> BaseListResult:
        """Абстрактный метод для получения данных из Elasticsearch."""

    def _get_sorting_body(self) -> dict:
        """Метод формирует возможное тело сортировки для поиска данных."""
        sort_body = {
            'sort': []
        }
        sort = sort_body.get('sort')

        for field_sorting in self._sorting:
            sort.append({field_sorting.name: field_sorting.order_type.value})

        return sort_body
