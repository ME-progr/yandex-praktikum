"""Модуль описывает ETL процесс"""

from logging import Logger

import backoff
from confluent_kafka.error import KafkaError
from clickhouse_driver.errors import Error

from services.interfaces import BaseBrokerExtractor, BaseDatabaseLoader, BaseExtractorAdapter
from storages.broker.topics import topics_list
from utils.connection import Clients
from utils.constants import LoggerMessage
from utils.converter import generated_cache_key
from utils.db import init_storages
from utils.exceptions import LoadDatasError


class ETL:
    def __init__(
            self,
            extractor: BaseBrokerExtractor,
            loader: BaseDatabaseLoader,
            adapter: BaseExtractorAdapter
    ):
        self._extractor = extractor
        self._adapter = adapter
        self._loader = loader
        self._adapter = adapter

    @backoff.on_exception(backoff.expo, exception=(KafkaError, Error))
    def __enter__(self):
        init_storages()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        return False if exc_type else True

    @backoff.on_exception(backoff.expo, exception=LoadDatasError)
    def start(self, logger: Logger):
        """Метод запускает процесс переноса данных"""
        while True:
            for topic in topics_list:
                datas_from_broker = self._extractor.extract(topic)
                if not datas_from_broker:
                    logger.info(LoggerMessage.NO_EVENTS.value)
                    continue

                adapted_datas = self._adapter.adapt(datas_from_broker)
                is_saved = saving_process(self._loader.load)('ugc.film_view', adapted_datas)
                if not is_saved:
                    logger.error(LoggerMessage.ERROR_SAVE.value)
                    raise LoadDatasError

                self._save_next_offset(self._adapter.partitions_offset)
                logger.info(LoggerMessage.SAVE_COMPLETE.value)

    @staticmethod
    def _save_next_offset(msg: dict) -> None:
        """
        Метод сохраняет `offset` последнего события

        Args:
            msg: последний `offset` у события топика
        """
        for partition, offset in msg.items():
            key, value = generated_cache_key(partition), offset
            Clients.kafka_redis.set_value(key, value)


def saving_process(func):
    """Декоратор пробует внести данные в БД. В случае успеха вернётся True, нет - False"""
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception:
            return False
        return True
    return wrapper
