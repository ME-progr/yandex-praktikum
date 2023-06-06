"""Модуль для работы с `Kafka`."""

from time import sleep

from confluent_kafka import TopicPartition
from confluent_kafka.admin import NewTopic

from core.config import kafka_settings
from storages.interfaces import StorageManager
from utils.connection import Clients
from utils.converter import generated_cache_key
from .topics import topics_list


class KafkaManager(StorageManager):

    def on_start_up(self) -> None:
        self._create_topics_if_not_exists()

    def on_shut_down(self):
        self.client.close()

    def read(self, topic: str) -> list | None:
        """
        Метод считывает полученные сообщения.

        Args:
            topic: название топика

        Returns:
            список свежий сообщений
        """
        partition = self._get_next_offset(topic)
        self.client.assign(partition)
        msg = self.client.consume(kafka_settings.batch_size, kafka_settings.timeout)

        return msg

    def _create_topic(self, topic_name: str) -> None:
        """
        Метод создаёт топик по названию

        Args:
            topic_name: наименование топика
        """

        topic_list = [NewTopic(topic=topic_name, num_partitions=kafka_settings.number_partitions, replication_factor=1)]
        self.client.create_topics(new_topics=topic_list, validate_only=False)
        sleep(1)

    def _create_topics_if_not_exists(self) -> None:
        """Метод проверят существование топиков в `Kafka`"""

        topics = self.client.list_topics().topics
        for topic_name in topics_list:
            if not topics.get(topic_name):
                self._create_topic(topic_name)

    @staticmethod
    def _get_next_offset(topic_name: str) -> list[TopicPartition]:
        """
        Метод возвращает `offset` для каждой партиции топика.

        Args:
            topic_name: наименование топика
        Returns:
            список с `offset` для партиций
        """
        return [
            TopicPartition(
                topic=topic_name,
                partition=partition,
                offset=Clients.kafka_redis.get_value(generated_cache_key(topic_name, partition)) + 1
            ) for partition in range(kafka_settings.number_partitions)
        ]
