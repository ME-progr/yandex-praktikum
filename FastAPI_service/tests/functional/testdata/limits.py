"""Модуль содержит различные тестовые данные для теста лимитов."""

from collections import namedtuple
from http import HTTPStatus


def get_test_data_for_wrong_limit():
    """Функция возвращает тестовые данные для тестирования некорректного лимита."""
    TestData = namedtuple('TestData', ['wrong_limit', 'expected_body', 'expected_status'])

    negative_limit_body = {
        'detail': [
            {
                'loc': ['query', 'limit'],
                'msg': 'ensure this value is greater than or equal to 1',
                'type': 'value_error.number.not_ge',
                'ctx': {'limit_value': 1}
            }
        ]
    }

    float_limit_body = {
        'detail': [
            {
                'loc': ['query', 'limit'],
                'msg': 'value is not a valid integer',
                'type': 'type_error.integer'
            }
        ]
    }

    return [
        TestData(
            wrong_limit=-1,
            expected_body=negative_limit_body,
            expected_status=HTTPStatus.UNPROCESSABLE_ENTITY,
        ),
        TestData(
            wrong_limit=0.5,
            expected_body=float_limit_body,
            expected_status=HTTPStatus.UNPROCESSABLE_ENTITY,
        ),
    ]
