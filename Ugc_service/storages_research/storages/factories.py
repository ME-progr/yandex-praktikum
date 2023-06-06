from clickhouse_driver import Client
from vertica_python import Connection

from storages_research.storages.interfaces import Storage, StorageManager
from storages_research.storages.clickhouse import ClickHouseManager, ClickHouseStorage
from storages_research.storages.vertica import VerticaManager, VerticaStorage

TClient = Client | Connection


def get_manager_by_client(client: TClient) -> StorageManager:
    """
    Фабрика менеджеров.

    Args:
        client: клиент для работы с базой данных.
    """
    if isinstance(client, Client):
        return ClickHouseManager(client)
    if isinstance(client, Connection):
        return VerticaManager(client)


def get_storage_by_client(client: TClient) -> Storage:
    """
    Фабрика хранилищ.

    Args:
        client: клиент для работы с базой данных.
    """
    if isinstance(client, Client):
        return ClickHouseStorage(client)
    if isinstance(client, Connection):
        return VerticaStorage(client)
