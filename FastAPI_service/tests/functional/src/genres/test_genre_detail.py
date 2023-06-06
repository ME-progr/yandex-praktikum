"""Модуль отвечает за тестирование детальной информации о жанрах."""

import pytest

from tests.functional.settings import settings
from tests.functional.testdata.genres import get_genre_existed_detail_data, get_genre_empty_detail_data
from tests.functional.utils.storages import write_data_to_es
from tests.functional.utils.api import api_request


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'test_data, expected_body, expected_status',
    get_genre_existed_detail_data(),
)
async def test_existed_genre_detail(
    es_client,
    api_session,
    admin_token,
    test_data,
    expected_body,
    expected_status,
):
    """
    Тест проверяет получение существующей детальной информации по жанру.

    Args:
        es_client: экземпляр клиента Elasticsearch.
        api_session: экземпляр клиентской сессии.
        admin_token: access token админа
        test_data: тестовые данные, с которыми будем работать.
        expected_body: ожидаемый ответ API.
        expected_status: ожидаемый статус ответа API.
    """
    genre_id = test_data.get('id')
    await write_data_to_es(es_client, settings.elastic_index.GENRES, [test_data])
    url = f'{settings.service_url}/api/v1/genres/{genre_id}'

    body, headers, status = await api_request(api_session, 'GET', url, token=admin_token)

    assert status == expected_status
    assert body == expected_body


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'test_data, expected_status',
    get_genre_empty_detail_data(),
)
async def test_empty_genre_detail(
    api_session,
    admin_token,
    test_data,
    expected_status,
):
    """
    Тест проверяет получение отсутствующей детальной информации по жанру.

    Args:
        api_session: экземпляр клиентской сессии.
        admin_token: access token админа
        test_data: тестовые данные, с которыми будем работать.
        expected_status: ожидаемый статус ответа API.
    """
    genre_id = test_data
    url = f'{settings.service_url}/api/v1/genres/{genre_id}'

    body, headers, status = await api_request(api_session, 'GET', url, token=admin_token)

    assert status == expected_status
