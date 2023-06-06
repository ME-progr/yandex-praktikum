"""Модуль отвечает за хранилище Clickhouse."""
from typing import Iterable

from storages_research.storages.interfaces import Storage, StorageManager
from storages_research.utils import iter_csv


class ClickHouseStorage(Storage):
    """Описывает работу с хранилищем ClickHouse"""

    name = 'ClickHouse'

    def get_data(self, query: str, chunk_size: int | None = None):
        if chunk_size:
            return self.client.execute_iter(query, chunk_size=chunk_size)

        return self.client.execute(query)

    def write_data(self, target: str, data: Iterable[dict]):
        query = f'INSERT INTO {target} VALUES'
        self.client.execute(query, data)

    def import_from_csv(self, target: str, file_path: str, converters: dict):
        self.write_data(target, iter_csv(file_path, converters))


class ClickHouseManager(StorageManager):
    """Менеджер для работы с базой"""

    def on_start_up(self):
        """Действия, которые должны производиться на старте приложения."""
        self._create_database()
        self._create_film_view_table()

    def on_shut_down(self):
        """Действия, которые должны производиться перед завершением работы приложения."""
        pass

    def _create_database(self):
        self.client.execute('CREATE DATABASE IF NOT EXISTS ugc ON CLUSTER company_cluster')

    def _create_film_view_table(self):
        self.client.execute(
            """
            CREATE OR REPLACE TABLE ugc.film_view
            ON CLUSTER company_cluster
            (
                user_id UUID,
                film_id UUID,
                film_frame Float64,
                created_at DateTime
            )
            Engine=MergeTree()
            ORDER BY (user_id, film_id, film_frame)
            """
        )
