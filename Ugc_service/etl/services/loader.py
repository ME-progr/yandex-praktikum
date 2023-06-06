"""Модуль для загрузки данных в `Clickhouse`"""

from clickhouse_driver import Client

from .interfaces import BaseDatabaseLoader
from storages.database.queries import INSERT_DATAS


class ClickhouseLoader(BaseDatabaseLoader):
    """Класс загрузки данных в `ClickHouse`."""

    def __init__(self, client: Client):
        super().__init__(client)

    def load(self, target: str, data: list) -> None:
        """
        Метод сохраняет данные в базу данных

        Args:
            target: название базы данных
            data: данные на запись
        """
        query = INSERT_DATAS.format(database=target)
        self._client.execute(query, data)
