"""Модуль содержит различные утилиты для работы со списковыми методами."""
import pymongo

from ugc_service.src.services.lists.sorting import Sorting, OrderType


def adapt_sorting_to_mongo_sort(sorting: Sorting) -> list[tuple[str, pymongo.ASCENDING | pymongo.DESCENDING]]:
    """
    Метод адаптирует сортировку к MongoDB формату.

    Args:
        sorting: сортировка.
    """
    adapted_sorting = []
    for sort in sorting:
        order_type = pymongo.ASCENDING if sort.order_type == OrderType.ASC else pymongo.DESCENDING
        adapted_sorting.append((sort.name, order_type))

    return adapted_sorting
