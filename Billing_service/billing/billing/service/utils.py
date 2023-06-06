"""Модуль содержит различные полезные утилиты."""

import inspect
from typing import Any


def is_attribute_in_class(obj: Any, attribute: str) -> bool:
    """
    Функция проверяет, входит ли аттрибут в атрибуты оьъекта.

    Args:
        obj: оьъект для проверки.
        attribute: атрибут, который нужно проверить.

    Return:
        True - существует, False - не существует.
    """
    attributes = inspect.getmembers(obj, lambda a: not (inspect.isroutine(a)))
    attributes_for_search = set(a[0] for a in attributes if not (a[0].startswith('__') and a[0].endswith('__')))
    return attribute in attributes_for_search
