"""Модуль содержит различные тестовые данные для событий."""

from uuid import uuid4
from random import getrandbits
from collections import namedtuple
from http import HTTPStatus


def get_film_frame_data() -> list:
    """Функция генерирует тестовые данные для тестирования записи времени фильма в Kafka."""
    TestData = namedtuple('TestData', ['film_id', 'film_frame', 'expected_status'])

    return [
        TestData(
            film_id=str(uuid4()),
            film_frame=getrandbits(50),
            expected_status=HTTPStatus.OK
        ),
        TestData(
            film_id=str(uuid4()),
            film_frame=None,
            expected_status=HTTPStatus.UNPROCESSABLE_ENTITY
        ),
        TestData(
            film_id=None,
            film_frame=getrandbits(50),
            expected_status=HTTPStatus.UNPROCESSABLE_ENTITY
        ),
        TestData(
            film_id=None,
            film_frame=None,
            expected_status=HTTPStatus.UNPROCESSABLE_ENTITY
        )
    ]
