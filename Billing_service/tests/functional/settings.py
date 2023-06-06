"""Модуль содержит настройки для тестов."""

import os
from functools import cached_property

from pydantic import BaseSettings, Field
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DEBUG_ENV = os.path.join(BASE_DIR, '.env.debug')
PROD_ENV = os.path.join(BASE_DIR, '.env.prod')

project_env = DEBUG_ENV


class Settings(BaseSettings):

    billing_host: str = Field(..., env='BILLING_HOST')
    billing_port: str = Field(..., env='BILLING_PORT')
    billing_header_host: str = Field(..., env='BILLING_HEADER_HOST')

    auth_host: str = Field(..., env='AUTH_HOST')
    auth_port: str = Field(..., env='AUTH_PORT')

    debug: str = Field(..., env='DEBUG')

    class Config:
        keep_untouched = (cached_property,)
        env_file = project_env


class DataBaseSettings(BaseSettings):
    """Класс настроек для подключения к БД"""

    billing_pg_username: str = Field(..., env='BILLING_POSTGRES_USER')
    billing_pg_password: str = Field(..., env='BILLING_POSTGRES_PASSWORD')
    billing_pg_host: str = Field(..., env='BILLING_DB_HOST')
    billing_pg_port: str = Field(..., env='BILLING_DB_PORT')
    billing_pg_name: str = Field(..., env='BILLING_POSTGRES_DB')
    billing_schema: str = Field(..., env='BILLING_DB_SCHEMA')

    auth_pg_username: str = Field(..., env='AUTH_POSTGRES_USER')
    auth_pg_host: str = Field(..., env='AUTH_DB_HOST')
    auth_pg_port: str = Field(..., env='AUTH_DB_PORT')
    auth_pg_password: str = Field(..., env='AUTH_POSTGRES_PASSWORD')
    auth_pg_name: str = Field(..., env='AUTH_POSTGRES_DB')
    auth_schema: str = Field(..., env='AUTH_DB_SCHEMA')

    class Config:
        env_file = project_env


settings = Settings()
DB_SETTINGS = DataBaseSettings()

BILLING_PG_DSL = {
    'database': DB_SETTINGS.billing_pg_name,
    'user': DB_SETTINGS.billing_pg_username,
    'password': DB_SETTINGS.billing_pg_password,
    'host': DB_SETTINGS.billing_pg_host,
    'port': DB_SETTINGS.billing_pg_port
}

AUTH_PG_DSL = {
    'database': DB_SETTINGS.auth_pg_name,
    'user': DB_SETTINGS.auth_pg_username,
    'password': DB_SETTINGS.auth_pg_password,
    'host': DB_SETTINGS.auth_pg_host,
    'port': DB_SETTINGS.auth_pg_port
}
