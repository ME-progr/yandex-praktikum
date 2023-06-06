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

project_env = DEBUG_ENV


class SourceData(str, Enum):
    """Класс описывает возможные источники данных."""

    ES_GENRES = 'genres'
    ES_MOVIES = 'movies'
    ES_PERSONS = 'persons'


class Settings(BaseSettings):
    project_name: str = Field(..., env='PROJECT_NAME')
    project_version: str = Field(..., env='PROJECT_VERSION')

    redis_host: str = Field(..., env='REDIS_HOST')
    redis_port: int = Field(..., env='REDIS_PORT')

    elastic_host: str = Field(..., env='ELASTIC_HOST')
    elastic_port: int = Field(..., env='ELASTIC_PORT')

    timeline_of_cache_seconds: int = Field(..., env='TIMELINE_OF_CACHE_SECONDS')
    timeline_of_cache_multiplier: int = Field(..., env='TIMELINE_OF_CACHE_MULTIPLIER')

    jwt_algorithm: str = Field(..., env='JWT_ALGORITHM')

    debug: str = Field(..., env='APP_DEBUG')

    source_data: type(SourceData) = SourceData

    @cached_property
    def timeline_of_cache(self):
        return self.timeline_of_cache_seconds * self.timeline_of_cache_multiplier

    class Config:
        keep_untouched = (cached_property,)
        env_file = project_env


class AuthSettings(BaseSettings):

    auth_host: str = Field(..., env='AUTH_HOST')
    auth_port: int = Field(..., env='AUTH_PORT')

    class Config:
        keep_untouched = (cached_property,)
        env_file = project_env


settings = Settings()
auth_settings = AuthSettings()

logging_config.dictConfig(LOGGING)
