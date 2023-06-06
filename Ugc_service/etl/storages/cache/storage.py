"""Модуль взаимодействия с кэш-хранилищем."""

from storages.interfaces import CacheStorage


class RedisStorage(CacheStorage):
    """Класс взаимодействия с `Redis`"""

    def __init__(self, client):
        super().__init__(client)

    def get_value(self, key: str) -> int:
        """Метод получает значение по ключу у хэш-хранилища"""
        cache_value = self._client.get(key)
        if cache_value:
            return int(cache_value.decode())
        return -1

    def set_value(self, key, value) -> None:
        """Метод сохраняет пару ключ-значение в кэш."""
        self._client.set(key, value)
