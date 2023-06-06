from contextlib import contextmanager
from pymongo import MongoClient
from clickhouse_driver import Client


@contextmanager
def clickhouse_context(host: str, port: str) -> Client:
    """
    Контектсный менеджер для открытия и закрытия подключения к Clickhouse.
    Args:
        host (str): хост.
        port (str): порт.
    Yields:
        соединение с БД.
    """
    client = Client(host=host, port=port)
    yield client
    client.disconnect_connection()


@contextmanager
def mongo_context(host1: str, host2: str) -> MongoClient:
    """
    Контектсный менеджер для открытия и закрытия подключения к Mongo.
    Args:
        host1 (str): хост.
        host2 (str): хост второго маршрутизатора.
    Yields:
        соединение с БД.
    """
    client = MongoClient(host=[host1, host2])
    yield client
    client.close()
