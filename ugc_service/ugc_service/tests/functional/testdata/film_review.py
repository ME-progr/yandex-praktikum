"""Модуль содержит различные тестовые данные для рейтинга фильмов."""

from uuid import uuid4
from collections import namedtuple
from http import HTTPStatus


def get_film_review_data() -> list:
    """Функция генерирует тестовые данные для тестирования записи времени фильма в Kafka."""
    TestData = namedtuple('TestData', ['film_id', 'review', 'expected_status'])
    return [
        TestData(
            film_id=str(uuid4()),
            review='test_review',
            expected_status=HTTPStatus.OK
        ),
        TestData(
            film_id=str(uuid4()),
            review='',
            expected_status=HTTPStatus.OK
        ),
        TestData(
            film_id='',
            review='test_review',
            expected_status=HTTPStatus.NOT_FOUND
        ),
        TestData(
            film_id='',
            review='',
            expected_status=HTTPStatus.NOT_FOUND
        ),
    ]


def get_film_id_data() -> list:
    """Функция генерирует тестовые данные для тестирования записи времени фильма в Kafka."""
    TestData = namedtuple('TestData', ['film_id', 'expected_status'])
    return [
        TestData(
            film_id=str(uuid4()),
            expected_status=HTTPStatus.OK
        ),
        TestData(
            film_id='',
            expected_status=HTTPStatus.NOT_FOUND
        ),
    ]
