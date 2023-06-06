"""Модуль для адаптирования данных `Kafka`."""
from collections import defaultdict

from confluent_kafka import Message

from utils.constants import ParserMessage
from .interfaces import BaseExtractorAdapter


class AdapterKafkaToClickhouse(BaseExtractorAdapter):
    """Класс адаптации данных `Kafka` для записи в `Clickhouse`"""

    def __init__(self):
        self.partitions_offset = defaultdict(int)

    def adapt(self, events: list) -> list:
        """
        Метод возвращает адаптированные данные.

        Args:
            events: события брокера-сообщений

        Returns:
            список адаптированных событий
        """
        adapted_datas = []

        for event in events:
            adapted_datas.append(self._adapt_processing(event))

        return adapted_datas

    def _adapt_processing(self, msg: Message) -> tuple:
        """Метод адаптирует полученное сообщение

        Args:
            msg: сообщение брокера

        Returns:
            адаптированные поля
        """
        msg_items = ParserMessage(msg)
        self.partitions_offset[f'{msg_items.topic}_{msg_items.partition}'] = msg_items.offset
        return msg_items.user_id, msg_items.film_id, msg_items.film_frame, msg_items.created_at
