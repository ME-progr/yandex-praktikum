"""Модуль отвечает за хранилище Clickhouse."""

from storages.interfaces import StorageManager
from .queries import CREATE_TABLE, CREATE_DATABASE


class ClickHouseManager(StorageManager):
    """Менеджер для работы с `ClickHouse`"""

    def on_start_up(self):
        """Действия, которые должны производиться на старте приложения."""
        self._create_database()
        self._create_film_view_table()

    def on_shut_down(self):
        """Действия, которые должны производиться перед завершением работы приложения."""
        self.client.disconnect_connection()

    def _create_database(self):
        self.client.execute(CREATE_DATABASE)

    def _create_film_view_table(self):
        self.client.execute(CREATE_TABLE)
