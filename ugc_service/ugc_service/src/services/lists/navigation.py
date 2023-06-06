"""Модуль содержит описание навигации для списковых методов."""
from dataclasses import dataclass


@dataclass
class Navigation:
    """Класс описывает навигацию"""

    page: int
    limit: int
    offset: int = 0

    def __post_init__(self):
        """В случае заданного номера страницы и лимита записей на странице автоматически рассчитываем offset."""
        if self.page and self.limit:
            self.offset = (self.page - 1) * self.limit
