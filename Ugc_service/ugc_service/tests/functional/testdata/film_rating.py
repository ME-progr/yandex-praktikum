"""Модуль содержит различные тестовые данные для рейтинга фильмов."""

from uuid import uuid4
from random import randint
from collections import namedtuple
from http import HTTPStatus


def get_film_rating_data() -> list:
    """Функция генерирует тестовые данные для тестирования записи времени фильма в Kafka."""
    TestData = namedtuple('TestData', ['film_id', 'rating', 'expected_status'])
    specific_film_id = '5f9699ce-4e73-4e50-89d6-4f29dc207fb5'
    specific_rating = 9
    return [
        TestData(
            film_id=str(uuid4()),
            rating=randint(1, 10),
            expected_status=HTTPStatus.OK
        ),
        TestData(
            film_id=str(uuid4()),
            rating='',
            expected_status=HTTPStatus.UNPROCESSABLE_ENTITY
        ),
        TestData(
            film_id='',
            rating=randint(1, 10),
            expected_status=HTTPStatus.NOT_FOUND
        ),
        TestData(
            film_id='',
            rating='',
            expected_status=HTTPStatus.NOT_FOUND
        ),
        TestData(
            film_id=specific_film_id,
            rating=specific_rating,
            expected_status=HTTPStatus.OK
        ),
        TestData(
            film_id=specific_film_id,
            rating=specific_rating,
            expected_status=HTTPStatus.BAD_REQUEST
        )
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
