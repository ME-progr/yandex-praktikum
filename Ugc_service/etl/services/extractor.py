"""Модуль для выгрузки данных из 'Kafka'."""

from confluent_kafka import Consumer

from .interfaces import BaseBrokerExtractor
from storages.broker.kafka import KafkaManager


class KafkaExtractor(BaseBrokerExtractor):
    """Класс получения событий."""

    def __init__(self, consumer: Consumer) -> None:
        super().__init__(consumer)
        self._manager = KafkaManager(self._consumer)

    def extract(self, topic_name) -> list:
        """Метод вытаскивает события у топика."""
        return self._manager.read(topic_name)
