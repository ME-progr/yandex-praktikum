"""Модуль отвечающий за сущности, помогающие работать с сортировкой."""

from dataclasses import dataclass
from enum import Enum


class OrderType(str, Enum):
    """Класс отвечает за типы сортировок."""

    ASC = 'asc'
    DESC = 'desc'


@dataclass(frozen=True)
class FieldSorting:
    """Класс описывает сортировку для текущего поля."""

    name: str
    order_type: OrderType


class Sorting:
    """
    Класс описывает поля и тип сортировки, применяемый к полю.

    Сортировки полей должны добавляться в том порядке, в котором вы собираетесь их применять.
    """

    def __init__(self):
        """Инициализирующий метод."""
        self._fields_sorting: list[FieldSorting] = []

    def __iter__(self):
        """Итерация по сортировке."""
        return FieldSortingIterator(self)

    def __len__(self):
        """Длина сортировки."""
        return len(self._fields_sorting)

    def __getitem__(self, item):
        """Поиск по индексу."""
        return self._fields_sorting[item]

    def __setitem__(self, key, value):
        """Установка значения по индексу."""
        self._fields_sorting[key] = value

    def __bool__(self) -> bool:
        """Булевые данные о структуре."""
        return bool(self._fields_sorting)

    def append_field_sorting(self, field_name: str, order_type: OrderType):
        """
        Метод добавляет сортировку для указанного поля в общий пул сортировок.

        Args:
            field_name: наименование поля.
            order_type: тип сортировки.
        """
        if not self._update_field_order_type_if_exists(field_name, order_type):
            self._fields_sorting.append(FieldSorting(field_name, order_type))

    def append_str_field_sorting(self, sorting_field: str):
        """
        Метод добавляет сортировку для строковых полей, с типом сортировки передающимся как операция '-'.

        Пример sorting_field: -name => (name, OrderType.DESC), birth_date => (birth_date, OrderType.ASC)

        Args:
            sorting_field: строковое поле для добавления сортировки.
        """
        if sorting_field.startswith('-'):
            self.append_field_sorting(sorting_field[1:], OrderType.DESC)
        else:
            self.append_field_sorting(sorting_field, OrderType.ASC)

    def remove_field_from_sorting(self, field_name: str):
        """
        Метод удаляет поле из сортировки.

        Args:
            field_name: наименование поля.
        """
        for index, field in enumerate(self._fields_sorting):
            if field.name == field_name:
                index_for_delete = index
                break
        else:
            return None
        del self._fields_sorting[index_for_delete]

    def update_field_name(self, old_name: str, new_name: str):
        """
        Обновляет наименование поля для сортировки.

        Args:
            old_name: старое наименование.
            new_name: новое наименование.
        """
        start_index = len(self) - 1
        while start_index >= 0:
            field = self[start_index]
            if field.name == old_name:
                self[start_index] = FieldSorting(name=new_name, order_type=field.order_type)
                start_index -= 1

    def fields_names(self) -> set[str]:
        """Метод возвращает наименование полей, по которым проходит сортировка."""
        return set(field.name for field in self._fields_sorting)

    def _update_field_order_type_if_exists(self, field_name: str, order_type) -> bool:
        """
        Метод обновляет тип сортировки для поля, если оно уже есть в текущем пуле сортировок.

        Args:
            field_name: наименование поля.
            order_type: тип сортировки.

        Returns:
            True - поле существовало и было обновлено. False - поле не существовало.
        """
        existed_index = self._get_index_for_field(field_name)
        if existed_index is not None:
            self._fields_sorting[existed_index] = FieldSorting(field_name, order_type)
            return True
        return False

    def _get_index_for_field(self, field_name: str) -> int:
        """Метод определяет индекс для наименования поля, если оно есть в списке сортировки."""
        for index, field_sorting in enumerate(self._fields_sorting):
            if field_sorting.name == field_name:
                return index


class FieldSortingIterator:
    """Класс обеспечивает итерацию по сортировкам."""

    def __init__(self, sorting: Sorting):
        """Инициализирующий метод для сортировки"""
        self._sorting = sorting
        self._current_index = 0

    def __next__(self):
        """Итерация по объекту сортировки."""
        while self._current_index < len(self._sorting):
            self._current_index += 1
            return self._sorting[self._current_index - 1]
        raise StopIteration
