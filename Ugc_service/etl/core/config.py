"""Модуль настроек."""

import os
import socket
from logging import INFO
from pathlib import Path

from pydantic import BaseSettings, Field

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DEV_ENV = os.path.join(BASE_DIR, 'etl', 'core', '.env.dev')

BASE_LOGGER_NAME = 'logger'

BASE_FORMAT = '%(name)s %(asctime)s %(levelname)s %(message)s'

BASE_LOG_LEVEL = INFO


class KafkaSettings(BaseSettings):
    """Класс настроек для `Kafka`"""

    kafka_dsn: str = Field(..., env='KAFKA_DSN')
    host: str = Field(..., env='KAFKA_HOST')
    port: int = Field(..., env='KAFKA_PORT')
    group_id: str = Field(..., env='KAFKA_GROUP_ID')
    auto_offset_reset: str = Field(..., env='KAFKA_AUTO_OFFSET_RESET')

    redis_host: str = Field(..., env='REDIS_KAFKA_HOST')
    redis_port: int = Field(..., env='REDIS_KAFKA_PORT')

    number_partitions: int = Field(..., env='KAFKA_NUMBER_PARTITIONS')
    batch_size: int = Field(..., env='KAFKA_BATCH_SIZE')
    timeout: float = Field(..., env='KAFKA_TIMEOUT')

    class Config:
        env_file = DEV_ENV


class ClickHouseSettings(BaseSettings):
    """Класс настроек для ClickHouse"""

    host: str = Field(..., env='CLICKHOUSE_HOST')
    port: int = Field(..., env='CLICKHOUSE_PORT')
    db_name: str = Field(..., env='CLICKHOUSE_DB_NAME')

    class Config:
        env_file = DEV_ENV


kafka_settings = KafkaSettings()
clickhouse_settings = ClickHouseSettings()


def kafka_consumer_settings() -> dict:
    """Метод возвращает набор параметров для Consumer-клиента Кафки"""
    consumer = {
        "bootstrap.servers": kafka_settings.kafka_dsn,
        "group.id": kafka_settings.group_id,
        "auto.offset.reset": kafka_settings.auto_offset_reset,
        "enable.auto.offset.store": False,
    }
    return consumer


def kafka_producer_settings() -> dict:
    """Метод возвращает набор параметров для Producer-клиента Кафки"""
    producer = {
        "bootstrap.servers": kafka_settings.kafka_dsn,
        'client.id': socket.gethostname()
    }
    return producer


def kafka_admin_settings() -> dict:
    """Метод возвращает набор параметров для Admin-клиента Кафки"""
    admin = {"bootstrap.servers": kafka_settings.kafka_dsn}
    return admin
