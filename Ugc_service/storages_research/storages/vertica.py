"""Модуль отвечает за хранилище Clickhouse."""
from typing import Iterable

from storages_research.storages.interfaces import Storage, StorageManager
from storages_research.utils import iter_csv


class VerticaStorage(Storage):
    """Описывает работу с хранилищем Vertica."""

    name = 'Vertica'

    def get_data(self, query: str, chunk_size: int | None = None):
        cursor = self.client.cursor()
        if chunk_size:
            return cursor.execute(query).fetchmany(chunk_size)

        return cursor.execute(query).fetchall()

    def write_data(self, target: str, data: Iterable[dict]):
        cursor = self.client.cursor()
        query = f'INSERT INTO {target} (user_id, film_id, film_frame, created_at) VALUES (?, ?, ?, ?)'

        batch_size = 1000
        batch_data = []
        for n, row in enumerate(data, 1):
            if isinstance(row, dict):
                batch_data.append(tuple(row.values()))
            else:
                batch_data.append(row)

            if n % batch_size == 0:
                cursor.executemany(query, batch_data, use_prepared_statements=True)
                batch_data = []

        if batch_data:
            cursor.executemany(query, batch_data, use_prepared_statements=True)

    def import_from_csv(self, target: str, file_path: str, converters: dict):
        cursor = self.client.cursor()
        cursor.execute(f"""
            COPY {target} FROM LOCAL
            '{file_path}' DELIMITER ','
        """)


class VerticaManager(StorageManager):
    """Менеджер для работы с базой"""

    def on_start_up(self):
        """Действия, которые должны производиться на старте приложения."""
        self._create_schema()
        self._create_film_view_table()

    def on_shut_down(self):
        """Действия, которые должны производиться на старте приложения."""
        self._drop_schema()

    def _create_schema(self):
        cursor = self.client.cursor()
        cursor.execute("""CREATE SCHEMA IF NOT EXISTS ugc;""")

    def _drop_schema(self):
        cursor = self.client.cursor()
        cursor.execute("""DROP SCHEMA IF EXISTS ugc CASCADE;""")

    def _create_film_view_table(self):
        cursor = self.client.cursor()
        cursor.execute(
            """
            CREATE TABLE ugc.film_view
            (
                user_id UUID NOT NULL,
                film_id UUID NOT NULL,
                film_frame FLOAT,
                created_at DateTime
            )
            """
        )

