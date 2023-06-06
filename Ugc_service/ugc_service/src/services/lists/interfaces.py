"""Модуль содержит базовую реализацию интерфейсов для списковых методов."""
from abc import ABC

from ugc_service.src.models.response_models import ListResponse
from ugc_service.src.services.lists.navigation import Navigation
from ugc_service.src.services.lists.sorting import Sorting


class BaseList(ABC):
    """Класс описывает интерфейс для списковых методов."""

    __slots__ = ('filter', 'navigation', 'sorting')

    def __init__(
            self,
            list_filter: dict | None = None,
            navigation: Navigation | None = None,
            sorting: Sorting | None = None
    ):
        self.filter = list_filter
        self.navigation = navigation
        self.sorting = sorting

    async def get(self) -> ListResponse:
        """Получает результаты спискового методы."""

        raise NotImplementedError('Необходимо добавить свою реализацию')
