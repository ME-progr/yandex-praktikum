"""Модуль содержит настройки для работы FastApi-приложения."""

import os
from enum import Enum
from logging import config as logging_config
from functools import cached_property

from pydantic import BaseSettings, Field
from pathlib import Path

from .logger import LOGGING


BASE_DIR = Path(__file__).resolve().parent.parent
DEBUG_ENV = os.path.join(BASE_DIR, 'core', '.env.debug')
PROD_ENV = os.path.join(BASE_DIR, 'core', '.env.prod')

project_env = PROD_ENV


class TopicName(Enum):

    FRAMERATE = 'framerate'


class CollectionName(Enum):
    """Класс определяет название коллекций для работы с mongo"""

    FilmRating = 'film_rating'
    FilmReview = 'film_review'
    UserBookmark = 'user_bookmark'


class DatabaseName(Enum):
    """Класс определяет название баз данных для работы с mongo"""

    UGC = 'ugc'


class Settings(BaseSettings):

    project_name: str = Field(..., env='PROJECT_NAME')
    project_version: str = Field(..., env='PROJECT_VERSION')

    redis_host: str = Field(..., env='REDIS_HOST')
    redis_port: int = Field(..., env='REDIS_PORT')

    timeline_of_cache: int = Field(..., env='TIMELINE_OF_CACHE')

    sentry_dsn: str = Field(..., env='SENTRY_DSN')

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

    mongos1_host: str = Field(..., env='MONGOS1_HOST')
    mongos1_port: int = Field(..., env='MONGOS1_PORT')

    mongos2_host: str = Field(..., env='MONGOS2_HOST')
    mongos2_port: int = Field(..., env='MONGOS2_PORT')

    db_name: str = Field(..., env='MONGO_DATABASE')
    username: str = Field(..., env='MONGO_USERNAME')
    password: str = Field(..., env='MONGO_PASSWORD')
    timeout_ms: int = Field(..., env='MONGO_TIMEOUT_MS')

    class Config:
        env_file = project_env


class JWTSettings(BaseSettings):
    """Класс настроек для JWT-токенов"""

    secret_key: str = Field(..., env='JWT_SECRET_KEY')
    algorithm: str = Field(..., env='JWT_ALGORITHM')

    class Config:
        env_file = project_env


settings = Settings()
kafka_settings = KafkaSettings()
clickhouse_settings = ClickHouseSettings()
mongodb_settings = MongoDBSettings()
jwt_settings = JWTSettings()

logging_config.dictConfig(LOGGING)
