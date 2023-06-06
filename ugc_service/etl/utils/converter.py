"""Модуль преобразования данных."""


def generated_cache_key(*args) -> str:
    """Метод возвращает сгенерированный ключ."""
    return '_'.join(map(str, args))
