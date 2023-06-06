"""Модуль с наименованиями топиков."""

from enum import Enum


class TopicName(str, Enum):
    FRAMERATE = 'framerate'


topics_list = [topic_name.value for topic_name in TopicName]
