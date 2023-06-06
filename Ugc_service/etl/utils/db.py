"""Модуль подключения хранилищ."""

from storages.broker.kafka import KafkaManager
from utils.connection import Clients
from storages.database.clickhouse import ClickHouseManager


def init_storages() -> None:
    """Для работы с хранилищами модуль инициализирует их."""
    KafkaManager(Clients.kafka_admin).on_start_up()
    ClickHouseManager(Clients.clickhouse).on_start_up()
