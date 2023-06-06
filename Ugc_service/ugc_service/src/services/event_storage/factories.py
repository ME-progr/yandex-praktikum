"""Модуль для представления Event Storage."""

import logging
from functools import lru_cache

from aiokafka import AIOKafkaProducer

from ugc_service.src.services.types import TEventWriterClient
from ugc_service.src.services.event_storage.interfaces import BaseEventWriter
from ugc_service.src.services.event_storage.kafka_producer import KafkaEventWriter


@lru_cache()
def get_event_writer_by_client(
        event_writer_client: TEventWriterClient,
) -> BaseEventWriter:
    """
    Функция предоставляет экземпляр класса сервиса хранилища событий на основе клиента.

    Args:
        event_writer_client - клиент хранилища событий для записи.

    Returns:
        BaseEventWriter
    """

    if isinstance(event_writer_client, AIOKafkaProducer):
        return KafkaEventWriter(event_writer_client)

    msg = 'Некорректный клиент хранилища событий для записи.'
    logging.error(msg)
    raise ValueError(msg)
