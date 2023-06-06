"""Модуль содержит различные тестовые данные для сервиса биллинга."""

from http import HTTPStatus
from collections import namedtuple


def get_create_subscribe_data() -> list:
    """Функция генерирует тестовые данные для тестирования записи времени фильма в Kafka."""
    TestData = namedtuple('TestData', ['query', 'expected_body', 'expected_status'])

    return [
        TestData(
            query={'subscribe_type': 'SU'},
            expected_body='https://checkout.stripe.com/c/pay/cs_test',
            expected_status=HTTPStatus.OK
        ),
        TestData(
            query={'subscribe_type': 'AM'},
            expected_body='https://checkout.stripe.com/c/pay/cs_test',
            expected_status=HTTPStatus.OK
        ),
    ]


def get_incorrect_create_subscribe_data() -> list:
    """Функция генерирует тестовые данные для тестирования записи времени фильма в Kafka."""
    TestData = namedtuple('TestData', ['query', 'expected_body', 'expected_status'])

    return [
        TestData(
            query={},
            expected_body={'subscribe_type': ['Обязательное поле.']},
            expected_status=HTTPStatus.BAD_REQUEST
        ),
        TestData(
            query={'subscribe_type': 'bad_value'},
            expected_body={'subscribe_type': ['"bad_value" is not a valid choice.']},
            expected_status=HTTPStatus.BAD_REQUEST
        ),
    ]
