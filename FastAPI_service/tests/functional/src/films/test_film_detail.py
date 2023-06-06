"""Модуль отвечает за тестирование детальной информации о фильмах."""

import pytest

from tests.functional.settings import settings
from tests.functional.testdata.films import get_test_data_for_film_detail, get_status_for_not_exist_film
from tests.functional.utils.storages import write_data_to_es
from tests.functional.utils.api import api_request


@pytest.mark.parametrize(
    'test_data, expected_body, expected_status',
    get_test_data_for_film_detail()
)
@pytest.mark.asyncio
async def test_exists_film_detail_response(
    es_client,
    api_session,
    test_data,
    admin_token,
    expected_body,
    expected_status
):
    """
    Тест проверяет при обращении к API-ручке конкретного фильма при существующей записи в БД:
        - статус запроса;
        - тело запроса.

    Args:
        es_client: экземпляр клиента Elasticsearch.
        api_session: экземпляр клиентской сессии.
        test_data: тестовые данные
        admin_token: access token админа
        expected_body: ожидаемый ответ API
        expected_status: ожидаемый статус ответа API
    """
    film_id = test_data.get('id')
    await write_data_to_es(es_client, settings.elastic_index.MOVIES, [test_data])
    url = f"{settings.service_url}/api/v1/films/{film_id}"

    body, _, status = await api_request(api_session, 'GET', url, token=admin_token)

    assert status == expected_status
    assert body == expected_body


@pytest.mark.parametrize(
    'film_id, expected_status',
    get_status_for_not_exist_film()
)
@pytest.mark.asyncio
async def test_not_exists_film_detail_response(
        api_session,
        admin_token,
        film_id,
        expected_status
):
    """
    Тест проверяет статус запроса при обращении к API-ручке конкретного фильма при несуществующей записи БД.

    Args:
        api_session: экземпляр клиентской сессии.
        admin_token: access token админа
        film_id: тестовый `id` фильма
        expected_status: ожидаемый статус ответа API
    """
    url = f'{settings.service_url}/api/v1/films/{film_id}'

    body, _, status = await api_request(api_session, 'GET', url, token=admin_token)

    assert status == expected_status
