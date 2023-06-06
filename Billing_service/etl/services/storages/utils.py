"""Модуль содержит api для работы хранилищами."""

from .key_value_storages import KeyValueStorageFactory
from .key_value_decorators import BackoffKeyValueDecorator


def get_backoff_key_value_storage(client, *args, **kwargs) -> BackoffKeyValueDecorator:
    """
    Функция инициализирует отказоустойчивой key-value хранилище.

    Args:
        client: клиент key-value хранилища.
        args: позиционные аргументы
        kwargs: именнованные аргументы.

    Returns:
        отказоустойчивое хланилище.
    """

    state_storage = KeyValueStorageFactory.storage_by_client(client, *args, **kwargs)
    return BackoffKeyValueDecorator(state_storage)
