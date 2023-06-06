"""Модуль константных значений."""

from dataclasses import dataclass
from enum import Enum
from uuid import UUID
from datetime import datetime

from confluent_kafka import Message


@dataclass
class ParserMessage:
    """Класс-парсер сообщения."""

    msg: Message
    user_id: UUID = None
    film_id: UUID = None
    film_frame: float = None
    partition: int = None
    offset: int = None
    topic: str = None
    created_at: datetime = None

    def __post_init__(self):
        user_id, film_id = self._parse_key(self.msg.key())
        self.created_at = self._time_convert(self.msg.timestamp())
        self.user_id, self.film_id = UUID(user_id), UUID(film_id)
        self.film_frame = float(self.msg.value().decode())
        self.partition, self.offset, self.topic = int(self.msg.partition()), int(self.msg.offset()), self.msg.topic()

    @staticmethod
    def _parse_key(event: bytes) -> list:
        """
        Метод разделения события на пару ключ-значение

        Args:
            event: событие

        Returns:
            список из ключа и значения
        """
        return event.decode().split('+')

    @staticmethod
    def _time_convert(data: tuple) -> datetime:
        """
        Метод перевода `timestamp` в `datetime`

        Args:
            data: кортеж из 2-ух параметров: тип `timestamp`, сам `timestamp`

        Returns:
            время события
        """

        _, timestamp = data
        return datetime.fromtimestamp(timestamp // 1_000)


class LoggerMessage(str, Enum):
    """Класс описывает msg логгера при работе `ETL`"""

    NO_EVENTS = 'No events!'
    ERROR_SAVE = 'Batch didn\'t save!'
    SAVE_COMPLETE = 'Batch was save'
