"""Модуль для работы с Kafka."""

import logging
from http import HTTPStatus

from aiokafka import AIOKafkaProducer
from aiokafka.errors import KafkaError
from fastapi import HTTPException


kafka_producer_client: AIOKafkaProducer | None = None


async def get_kafka_producer_client() -> AIOKafkaProducer:
    """функция возвращает синициализированный клиент Kafka Producer."""

    return kafka_producer_client


async def start_kafka_producer():
    """Соединение Kafka Producer c Kafka."""

    try:
        await kafka_producer_client.start()
    except KafkaError as error:
        logging.error(f'Ошибка соединения с Kafka: {error}')
        await kafka_producer_client.stop()
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=f'Ошибка соединения с Kafka.')

    logging.info('Успешное соединение Kafka Producer c Kafka.')

