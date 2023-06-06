"""Модуль содержит различные кастомные типы для работы сервисов."""
from typing import Union

from aioredis import Redis
from motor.motor_asyncio import AsyncIOMotorClient
from aiokafka import AIOKafkaProducer

CacheClient = Union[Redis]
TStorageClient = Union[AsyncIOMotorClient]
TEventWriterClient = Union[AIOKafkaProducer]

