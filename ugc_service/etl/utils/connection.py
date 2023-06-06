"""Модуль содержит утилиты для работы ETL процесса"""

from dataclasses import dataclass

from clickhouse_driver import Client
from confluent_kafka import Consumer, Producer
from confluent_kafka.admin import AdminClient
from redis import Redis

from core.config import (clickhouse_settings, kafka_settings, kafka_consumer_settings, kafka_admin_settings,
                         kafka_producer_settings)
from storages.cache.storage import RedisStorage


@dataclass
class Clients:
    """Класс описывает подключения к хранилищам"""
    clickhouse = Client(host=clickhouse_settings.host, port=clickhouse_settings.port)
    kafka_admin = AdminClient(kafka_admin_settings())
    kafka_consumer = Consumer(kafka_consumer_settings())
    kafka_producer = Producer(kafka_producer_settings())
    kafka_redis = RedisStorage(Redis(host=kafka_settings.redis_host, port=kafka_settings.redis_port))
