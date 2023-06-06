"""Модуль для работы с кэш-хранилищами"""

import json
from abc import ABC, abstractmethod
from functools import lru_cache
from hashlib import sha256

from aioredis import Redis
from fastapi.encoders import jsonable_encoder

from core.config import settings
from .exceptions import MissCacheInterfaceRealisation

CacheClient = Redis


class BaseCache(ABC):
    """Интерфейс для кэш-хранилищей."""

    def __init__(self, client):
        """
        Инициализирующий метод.

        Args:
            client: клиент кэша.
        """
        self._client = client

    @abstractmethod
    async def get(self, cache_id):
        """
        Абстрактный метод для получения кэш-значения по кэш-ключу.

        Args:
            cache_id (str): кэш-ключ
        """
        pass

    @abstractmethod
    async def put(self, cache_id, data, expire: int = settings.timeline_of_cache):
        """
        Абстрактный метод, для сохранения в кэш-хранилище значение по кэш-ключу

        Args:
            cache_id (str): кэш-ключ
            data (Any): значение
            expire: время жизни кэша
        """
        pass

    @staticmethod
    @abstractmethod
    async def make_cache_id_by_template(class_name, func_name, *args, **kwargs):
        """
        Метод формирует ключ для кэш-хранилища по заданным параметрам
        Args:
            class_name: название класса
            func_name: название функции
            *args: позиционные аргументы
            **kwargs: именованные аргументы

        Returns:
            кэш-ключ
        """
        pass


class RedisCache(BaseCache):
    """Класс для взаимодействия `Redis` хранилищем."""

    async def get(self, cache_id) -> dict | None:
        """
        Метод достает по кэш-ключу его значение.

        Args:
            cache_id (str): кэш-ключ

        Returns:
            dict
        """
        data: bytes = await self._client.get(cache_id)
        if data:
            return json.loads(data)

    async def put(self, cache_id, data, expire: int = settings.timeline_of_cache) -> None:
        """
        Метод сохраняет в кэш новую пару ключ-значение.

        Args:
            cache_id (str): кэш-ключ
            data (Any): значение кэш-ключа
            expire: время жизни кэша
        """
        cache_data = jsonable_encoder(data)
        await self._client.set(cache_id, json.dumps(cache_data), expire=expire)

    @staticmethod
    def make_cache_id_by_template(class_name: str, func_name: str, *args, **kwargs) -> str:
        """
        Метод генерирует ключ кэша по переданным параметрам.

        Args:
            class_name: наименование класса
            func_name: наименование функции
            args: позиционные аргументы
            kwargs: именованные аргументы

        Returns:
            cache_id
        """
        datas = f'{class_name}_{func_name}_{args}_{kwargs}'
        cache_id = sha256(datas.encode('utf-8')).hexdigest()
        return cache_id


@lru_cache()
def get_cache_by_client(client: CacheClient):
    """
    Singletone для инстанса кэша.

    Args:
        client: клиент кэша.
    """

    if isinstance(client, Redis):
        return RedisCache(client)

    raise MissCacheInterfaceRealisation(client)
