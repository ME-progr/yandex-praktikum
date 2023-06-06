"""Модуль содержит настройки для работы ETL."""
import os
from collections import namedtuple
from pathlib import Path
from enum import Enum
from pydantic import BaseSettings, Field

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
BASE_DIR = Path(__file__).resolve().parent.parent

StateStorageAdapterParams = namedtuple('StateStorageAdapterParams', ['storage_type', 'adapter_params'])

DEBUG_ENV = os.path.join(BASE_DIR, 'config', '.env.dev')
PROD_ENV = os.path.join(BASE_DIR, 'config', '.env.prod')

project_env = DEBUG_ENV


class RedisSetting(BaseSettings):
    """Класс отвечает за настройки редиса."""

    port: int = Field(..., env='REDIS_PORT')
    host: str = Field(..., env='REDIS_HOST')

    class Config:
        env_file = project_env


class MoviesDBSetting(BaseSettings):
    """Класс отвечает за настройки подключения к бд movie-admin."""

    name: str = Field(..., env='MOVIES_DB_NAME')
    user: str = Field(..., env='MOVIES_DB_USER')
    password: str = Field(..., env='MOVIES_DB_PASSWORD')
    host: str = Field(..., env='MOVIES_DB_HOST')
    port: int = Field(..., env='MOVIES_DB_PORT')

    def dsl(self) -> dict:
        return {
            'dbname': self.name,
            'user': self.user,
            'password': self.password,
            'host': self.host,
            'port': self.port,
        }

    class Config:
        env_file = project_env


class BillingDBSetting(BaseSettings):
    """Класс отвечает за настройки подключения к бд movie-admin."""

    name: str = Field(..., env='BILLING_DB_NAME')
    user: str = Field(..., env='BILLING_DB_USER')
    password: str = Field(..., env='BILLING_DB_PASSWORD')
    host: str = Field(..., env='BILLING_DB_HOST')
    port: int = Field(..., env='BILLING_DB_PORT')

    def dsl(self) -> dict:
        return {
            'dbname': self.name,
            'user': self.user,
            'password': self.password,
            'host': self.host,
            'port': self.port,
        }

    class Config:
        env_file = project_env


class Settings(BaseSettings):
    """Класс отвечает за базовые настройки."""

    time_to_restart_process: int = Field(..., env='TIME_TO_RESTART_PROCESSES_SECONDS')
    process_is_started_state: str = Field(..., env='PROCESS_IS_STARTED_STATE')
    date_format: str = Field(..., env='DATE_FORMAT')
    db_buffer_size: int = Field(..., env='DB_BUFFER_SIZE')

    class Config:
        env_file = project_env


class ETLProcessType(str, Enum):
    """Тип доступных ETL процессов."""

    MOVIE_FILMWORK = 'movie_filmwork'
    BILLING_FILMWORK = 'billing_filmwork'


class QueryType(str, Enum):
    """Клас описывает доступные типы запросов."""

    # для передачи данных из movie-admin в billing
    MOVIE_FILMWORK_SELECT = 'movie_filmwork_select'
    # для передачи данных из billing в movie-admin
    BILLING_FILMWORK_SELECT = 'billing_filmwork_select'
    BILLING_FILMWORK_UPDATE = 'billing_filmwork_update'


MODIFIED_STATE = {
    ETLProcessType.MOVIE_FILMWORK: 'modified_movie_filmwork',
    ETLProcessType.BILLING_FILMWORK: 'modified_billing_filmwork',
}

redis_settings = RedisSetting()
movies_db_settings = MoviesDBSetting()
billing_db_settings = BillingDBSetting()
settings = Settings()
