"""Модуль для представления Kafka Producer."""

import logging
from http import HTTPStatus

from fastapi import HTTPException
from aiokafka.errors import KafkaError, KafkaTimeoutError

from ugc_service.src.services.event_storage.interfaces import BaseEventWriter


class KafkaEventWriter(BaseEventWriter):
    """Класс отвечает за доступные действия с Kafka Producer клиентом."""

    async def write_event(self, topic: str, key: str, value: str):
        """
        Метод для записи события в Kafka.

        Args:
            topic (str): наименование топика для записи.
            key: (str): ключ для записи.
            value: (str): значение для записи.
        """

        try:
            response = await self._event_storage_client.send_and_wait(
                topic=topic,
                key=key.encode('utf-8'),
                value=value.encode('utf-8')
            )

        except KafkaTimeoutError as error:
            logging.error(f'Превышено время ответа при записи в Kafka. {error}')
            raise HTTPException(status_code=HTTPStatus.REQUEST_TIMEOUT, detail='Превышено время ответа при записи в Kafka.')

        except KafkaError as error:
            logging.error(f'Ошибка записи в Kafka. {error}')
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail='Ошибка записи в Kafka.')

        logging.info(
            f'Произведена запись в Kafka: \n\ttopic: {topic}, key: {key},  value: {value}, response: {response}.'
        )
