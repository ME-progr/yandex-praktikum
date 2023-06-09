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
PROD_ENV = os.path.join(BASE_DIR, 'core', '.env.prod.prod')

project_env = DEBUG_ENV


class CollectionName(Enum):
    """Класс определяет название коллекций для работы с mongo"""

    USER_PROFILE = 'user_profile'


class DatabaseName(Enum):
    """Класс определяет название баз данных для работы с mongo"""

    PROFILES = 'profiles'


class UserRole(Enum):
    """Класс описывает пользовательские роли."""

    ADMIN = 'admin'


class Settings(BaseSettings):

    project_name: str = Field(..., env='PROJECT_NAME')
    project_version: str = Field(..., env='PROJECT_VERSION')

    redis_host: str = Field(..., env='REDIS_HOST')
    redis_port: int = Field(..., env='REDIS_PORT')

    timeline_of_cache: int = Field(..., env='TIMELINE_OF_CACHE')

    debug: str = Field(..., env='DEBUG')

    class Config:
        keep_untouched = (cached_property,)
        env_file = project_env


class MongoDBSettings(BaseSettings):
    """Класс настроек для MongoDB"""

    mongos1_host: str = Field(..., env='MONGOS1_HOST')
    mongos1_port: int = Field(..., env='MONGOS1_PORT')

    mongos2_host: str = Field(..., env='MONGOS2_HOST')
    mongos2_port: int = Field(..., env='MONGOS2_PORT')

    db_name: str = Field(..., env='MONGO_DATABASE')
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
mongodb_settings = MongoDBSettings()
jwt_settings = JWTSettings()

logging_config.dictConfig(LOGGING)
