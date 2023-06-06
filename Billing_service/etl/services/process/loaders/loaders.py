"""Модуль отвечает за описание Загрузчиков данных в целевую базу."""

from abc import ABC, abstractmethod
from typing import Iterable

import psycopg2
from psycopg2.extras import execute_batch
from pydantic import BaseModel

from etl.services.logs.logs_setup import get_logger
from etl.config.settings import settings
from ..queries.queries import BaseETLQuery
from ..validators.validators import ModelValidator

logger = get_logger()


class BaseLoader(ABC):
    """Базовый класс, отвечающий за загрузку данных в целевой объект."""

    @abstractmethod
    def load(self, data_for_load: Iterable[dict]):
        pass


class PostgresUpsertLoader(BaseLoader):
    """Класс отвечает за загрузку данных в постгре"""

    def __init__(
            self,
            client: psycopg2,
            target_model: type(BaseModel),
            target_table_name: str,
            conflict_fields: list[str] = None,
    ):
        """
        Инициализирующий метод.

        Args:
            client: клиент Elasticsearch.
            target_index: целевой индекс для загрузки.
            validator: валидатор загружаемых данных.
        """
        self._client = client
        self._cursor = self._client.cursor()
        self._target_model = target_model
        self._target_table_name = target_table_name
        self._validator = ModelValidator(self._target_model)
        self._conflict_fields = conflict_fields

    @property
    def _target_field_names(self):
        return list(self._target_model.__fields__.keys())

    @property
    def _placeholders(self):
        return ','.join('%s' for _ in range(len(self._target_field_names)))

    @property
    def _sql_target_field_names(self):
        return ",".join(self._target_field_names)

    @property
    def _sql_conflict_condition(self):
        if not self._conflict_fields:
            return """ON CONFLICT DO NOTHING"""

        conflict_field_names = f'({",".join(self._conflict_fields)})'
        updated_field_names = (
            field_name for field_name in self._target_field_names if field_name not in conflict_field_names
        )
        set_condition = ','.join(f'{field_name} = EXCLUDED.{field_name}' for field_name in updated_field_names)

        return f"""
            ON CONFLICT {conflict_field_names} DO UPDATE
            SET {set_condition}
        """

    def load(self, data_for_load: Iterable[dict]):
        logger.info('Загружаем данные в Postgres.')
        sql = f"""
            INSERT INTO {self._target_table_name} ({self._sql_target_field_names})
            VALUES ({self._placeholders})
            {self._sql_conflict_condition}
        """
        logger.info(f'Сформированный запрос для всатвки данных в Postgres: {sql}')

        try:
            execute_batch(self._cursor, sql, self._get_valid_values(data_for_load), settings.db_buffer_size)
            self._client.commit()
        except Exception as error:
            self._client.rollback()
            logger.error(error)

        return True

    def _get_valid_values(self, data_for_load: Iterable[dict]):
        for row in self._validator.get_valid_data(data_for_load):
            yield tuple(row.get(field_name) for field_name in self._target_field_names)


class PostgreHardQueryLoader(BaseLoader):
    """Класс отвечает за загрузку данных в постгре c жестко заданным запросом"""

    def __init__(
            self,
            client: psycopg2,
            target_model: type(BaseModel),
            query: BaseETLQuery
    ):
        """
        Инициализирующий метод.

        Args:
            client: клиент Elasticsearch.
            target_index: целевой индекс для загрузки.
            validator: валидатор загружаемых данных.
        """
        self._client = client
        self._cursor = self._client.cursor()
        self._target_model = target_model
        self._validator = ModelValidator(self._target_model)
        self._query = query

    @property
    def _target_field_names(self):
        return list(self._target_model.__fields__.keys())

    def load(self, data_for_load: Iterable[dict]):
        logger.info('Загружаем данные в Postgres.')
        sql = self._query.get_sql()
        logger.info(f'Сформированный запрос для всатвки данных в Postgres: {sql}')

        try:
            execute_batch(self._cursor, sql, self._get_valid_values(data_for_load), settings.db_buffer_size)
            self._client.commit()
        except Exception as error:
            self._client.rollback()
            logger.error(error)

        return True

    def _get_valid_values(self, data_for_load: Iterable[dict]):
        for row in self._validator.get_valid_data(data_for_load):
            yield tuple(row.get(field_name) for field_name in self._target_field_names)
