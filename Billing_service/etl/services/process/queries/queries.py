"""Модуль отвечает за описание запросов для ETL-процесса."""
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from etl.config.settings import ETLProcessType, QueryType, MODIFIED_STATE
from etl.services.storages.key_value_storages import KeyValueStorage
from etl.services.logs.logs_setup import get_logger
from .pg_templates import MOVIES_QUERY, BILLING_QUERY

logger = get_logger()


class BaseETLQuery(ABC):
    """Базовый класс, для генерации запросов для ETL-процесса."""

    def __init__(self, process_type: ETLProcessType, state_storage: KeyValueStorage):
        """
        Инициализирующий метод.

        Args:
            process_type: Тип ETL-процесса
            state_storage: хранилище состояний для определения modified_state
        """
        self._process_type = process_type
        self._state_storage = state_storage
        self._modified_state_name = MODIFIED_STATE.get(self._process_type)

    @abstractmethod
    def get_sql(self) -> str:
        """
        Метод возвращает SQL, который нужно выполнить для получения данных.

        Returns:
            sql-запрос.
        """

    def _get_modified_state(self) -> Optional[datetime]:
        """
        Метод возвращает временное значение из хранилища для modified_state.

        Returns:
            modified_state: текущее значение moified_state в хранилище.
        """
        modified_state = self._state_storage.get_value(self._modified_state_name)
        logger.info(f'modified state для {self._process_type} равно: {modified_state}')
        return modified_state


class MoviesSelectETLQuery(BaseETLQuery):
    """Класс для генерации запроса по выгрузке данных из movie-admin"""

    def get_sql(self) -> str:
        """
        Метод возвращает SQL, который нужно выполнить для получения данных.

        Returns:
            sql-запрос.
        """
        logger.info(f'Генерируем запрос для {self._process_type}')
        query = MOVIES_QUERY.format(
            where_condition=self._get_where_condition(),
        )
        logger.info(f'Запрос к БД: \n {query}')

        return query

    def _get_where_condition(self) -> str:
        """
        Метод возвращает where условия для запроса.

        Returns:
            where для sql-запроса.
        """
        modified_state = self._get_modified_state()

        if modified_state is None:
            return 'WHERE TRUE'

        return "WHERE film_work.modified > '{modified_state}'::timestamp".format(
            modified_state=modified_state,
        )


class BillingMoviesSelectETLQuery(BaseETLQuery):
    """Класс для генерации запроса по выгрузке данных из billing"""

    def get_sql(self) -> str:
        """
        Метод возвращает SQL, который нужно выполнить для получения данных.

        Returns:
            sql-запрос.
        """
        logger.info(f'Генерируем запрос для {self._process_type}')
        query = BILLING_QUERY.format(
            where_condition=self._get_where_condition(),
        )
        logger.info(f'Запрос к БД: \n {query}')

        return query

    def _get_where_condition(self) -> str:
        """
        Метод возвращает where условия для запроса.

        Returns:
            where для sql-запроса.
        """
        modified_state = self._get_modified_state()

        if modified_state is None:
            return 'WHERE TRUE'

        return "WHERE fw.modified_subscribe_date > '{modified_state}'::timestamp".format(
            modified_state=modified_state,
        )


class BillingMoviesUpdateETLQuery(BaseETLQuery):
    """Класс для генерации запроса по обновлению данных в movie из billing"""

    def get_sql(self) -> str:
        """
        Метод возвращает SQL, который нужно выполнить для получения данных.

        Returns:
            sql-запрос.
        """
        return """
            UPDATE content.film_work
            SET subscribe_types = update_payload.subscribe_types::text[]
            FROM (VALUES (%s,%s)) as update_payload(id, subscribe_types)
            WHERE content.film_work.id::text = update_payload.id::text
        """


class ETLQueryFactory:
    """Фабрика классов для ETLQuery."""

    queries = {
        QueryType.MOVIE_FILMWORK_SELECT: MoviesSelectETLQuery,
        QueryType.BILLING_FILMWORK_SELECT: BillingMoviesSelectETLQuery,
        QueryType.BILLING_FILMWORK_UPDATE: BillingMoviesUpdateETLQuery,
    }

    @staticmethod
    def query_by_type(query_type: QueryType, *args, **kwargs) -> BaseETLQuery:
        """
        Метод возвращает инстанс запроса по заданному типу.

        Args:
            query_type: тип ETL процесса.
            args: позиционные аргументы.
            kwargs: именнованные аргументы.

        Returns:
            query (BaseETLQuery): запрос.
        """
        try:
            query_class = ETLQueryFactory.queries[query_type]
            return query_class(*args, **kwargs)
        except KeyError as error:
            logger.error(f'Для типа {query_type} не существует реализации запроса.', exc_info=True)
            raise error
