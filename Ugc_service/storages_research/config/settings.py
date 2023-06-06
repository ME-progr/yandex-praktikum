import os
from pathlib import Path

from pydantic import BaseSettings, Field

BASE_DIR = Path(__file__).resolve().parent.parent.parent

TEST_ENV = os.path.join(BASE_DIR, 'storages_research', 'config', '.env.tests')


class TestSettings(BaseSettings):
    """Класс настроек для тестов"""

    tests_count: int = Field(..., env='TESTS_COUNT')

    class Config:
        env_file = TEST_ENV


class ClickHouseSettings(BaseSettings):
    """Класс настроек для ClickHouse"""

    host: str = Field(..., env='CLICKHOUSE_HOST')
    port: int = Field(..., env='CLICKHOUSE_PORT')
    db_name: str = Field(..., env='CLICKHOUSE_DB_NAME')

    class Config:
        env_file = TEST_ENV


class VerticaSettings(BaseSettings):
    """Класс настроек для Vertica"""

    host: str = Field(..., env='VERTICA_HOST')
    port: int = Field(..., env='VERTICA_PORT')
    db_name: str = Field(..., env='VERTICA_DB_NAME')

    class Config:
        env_file = TEST_ENV


class MongoSettings(BaseSettings):
    """Класс настроек для Mongo"""

    host1: str = Field(..., env='MONGO_HOST1')
    host2: str = Field(..., env='MONGO_HOST2')
    mongo_test: bool = Field(..., env='MONGO_TEST')

    class Config:
        env_file = TEST_ENV


test_settings = TestSettings()
clickhouse_settings = ClickHouseSettings()
vertica_settings = VerticaSettings()
mongo_settings = MongoSettings()
vertica_connection_info = {
    'host': vertica_settings.host,
    'port': vertica_settings.port,
    'user': 'dbadmin',
    'password': '',
    'database': 'docker',
    'autocommit': True,
}
