"""Модуль отвечает за структуры данных, связанные с навигацией по результатам выборок."""

from enum import Enum
from typing import Any


class NavigationType(Enum):
    """Класс отвечает за тип навигации."""

    PAGINATION = 'pagination'
    SCROLL = 'scroll'
    SEARCH_AFTER = 'search_after'


class Navigation:
    """Класс-структура данных, который помогает работать с навигацией по списочным методам."""

    def __init__(
            self,
            nav_type: NavigationType,
            limit: int | None = None,
            offset: int | None = None,
            search_after: list[Any] | None = None,
    ):
        """
        Инициализирующий метод для навигации.

        Args:
            nav_type: тип навигации.
            limit: limit для навигации.
            offset: offset для навигации.
            search_after: ID курсора для навигации по курсору.
        """
        self.nav_type = nav_type
        self.limit = limit
        self.offset = offset
        self.search_after = search_after
