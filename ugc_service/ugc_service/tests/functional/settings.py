"""Модуль содержит настройки для тестов FastApi-приложения."""

import os
from enum import Enum
from functools import cached_property

from pydantic import BaseSettings, Field
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DEBUG_ENV = os.path.join(BASE_DIR, '.env.debug')
PROD_ENV = os.path.join(BASE_DIR, '.env.prod')

project_env = DEBUG_ENV


class TopicName(Enum):

    FRAMERATE = 'framerate'


class Settings(BaseSettings):

    project_name: str = Field(..., env='PROJECT_NAME')
    project_version: str = Field(..., env='PROJECT_VERSION')

    app_host: str = Field(..., env='APP_HOST')
    app_port: str = Field(..., env='APP_PORT')

    redis_host: str = Field(..., env='REDIS_HOST')
    redis_port: int = Field(..., env='REDIS_PORT')

    debug: str = Field(..., env='DEBUG')

    class Config:
        keep_untouched = (cached_property,)
        env_file = project_env


class KafkaSettings(BaseSettings):
    """Класс настроек для Kafka"""

    kafka_dsn: str = Field(..., env='KAFKA_DSN')
    host: str = Field(..., env='KAFKA_HOST')
    port: int = Field(..., env='KAFKA_PORT')
    group_id: str = Field(..., env='KAFKA_GROUP_ID')
    auto_offset_reset: str = Field(..., env='KAFKA_AUTO_OFFSET_RESET')
    timeout_ms: int = Field(..., env='KAFKA_TIMEOUT_MS')

    class Config:
        env_file = project_env


class ClickHouseSettings(BaseSettings):
    """Класс настроек для ClickHouse"""

    host: str = Field(..., env='CLICKHOUSE_HOST')
    port: int = Field(..., env='CLICKHOUSE_PORT')
    db_name: str = Field(..., env='CLICKHOUSE_DB_NAME')

    class Config:
        env_file = project_env


class MongoDBSettings(BaseSettings):
    """Класс настроек для MongoDB"""

    host: str = Field(..., env='MONGO_HOST')
    port: int = Field(..., env='MONGO_PORT')
    db_name: str = Field(..., env='MONGO_DATABASE')
    username: str = Field(..., env='MONGO_USERNAME')
    password: str = Field(..., env='MONGO_PASSWORD')
    timeout_ms: int = Field(..., env='MONGO_TIMEOUT_MS')

    class Config:
        env_file = project_env


settings = Settings()
kafka_settings = KafkaSettings()
clickhouse_settings = ClickHouseSettings()
mongodb_settings = MongoDBSettings()
