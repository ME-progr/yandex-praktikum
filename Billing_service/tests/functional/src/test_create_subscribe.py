"""Модуль отвечает за тестирование обработки событий."""

import pytest

from tests.functional.utils.api import api_request
from tests.functional.settings import settings
from tests.functional.testdata.billing_testdata import get_create_subscribe_data, get_incorrect_create_subscribe_data


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'query, expected_body, expected_status',
    get_create_subscribe_data(),
)
async def test_create_subscribe(
    api_session,
    prepared_tokens,
    query,
    expected_body,
    expected_status
):
    """Тестирование ручки предоставления ссылки на оплату подписки."""

    token = prepared_tokens.get('test_user').get('access_token')
    url = f'http://{settings.billing_host}:{settings.billing_port}/billing/api/v1/create-subscribe/'
    header_host = f'{settings.billing_header_host}:{settings.billing_port}'

    body, headers, status = await api_request(
        api_session,
        'POST',
        url,
        json=query,
        token=token,
        header_host=header_host)

    assert expected_body in body
    assert expected_status == status


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'query, expected_body, expected_status',
    get_incorrect_create_subscribe_data(),
)
async def test_incorrect_create_subscribe(
    api_session,
    prepared_tokens,
    query,
    expected_body,
    expected_status
):
    """Тестирование предоставления ссылки на оплату подписки с некорректными параметрами."""

    token = prepared_tokens.get('test_user').get('access_token')
    url = f'http://{settings.billing_host}:{settings.billing_port}/billing/api/v1/create-subscribe/'
    header_host = f'{settings.billing_header_host}:{settings.billing_port}'

    body, headers, status = await api_request(
        api_session,
        'POST',
        url,
        json=query,
        token=token,
        header_host=header_host)

    assert expected_body == body
    assert expected_status == status
