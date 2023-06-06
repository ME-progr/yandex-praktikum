import re

import pytest

from tests.functional.settings import settings
from tests.functional.testdata.persons import get_persons_data, generate_incorrect_input_for_search_persons
from tests.functional.utils.storages import write_data_to_es
from tests.functional.utils.api import api_request


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'query_data, test_data, expected_body, expected_status',
    get_persons_data(),
)
async def test_search_persons(
    es_client,
    api_session,
    admin_token,
    query_data,
    test_data,
    expected_body,
    expected_status
):
    """
    Тест проверяет поиск людей по заданным параметрам.

    Args:
        es_client: экземпляр клиента Elasticsearch.
        api_session: экземпляр клиентской сессии.
        admin_token: access token админа
        query_data: параметры запроса для получения ответа API.
        test_data: тестовые данные, с которыми будем работать.
        expected_body: ожидаемый ответ API.
        expected_status: ожидаемый статус ответа API.
    """
    await write_data_to_es(es_client, settings.elastic_index.PERSONS, test_data)
    url = f'{settings.service_url}/api/v1/persons/search'
    search_name = query_data.get('full_name')

    body, headers, status = await api_request(api_session, 'GET', url, params=query_data, token=admin_token)

    assert status == expected_status
    for person in body.get('result'):
        assert True if re.search(search_name, person.get('full_name')) else False


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'query_data, expected_body, expected_status',
    generate_incorrect_input_for_search_persons(),
)
async def test_incorrect_input_for_search_persons(
    api_session,
    admin_token,
    query_data,
    expected_body,
    expected_status
):
    """
    Тест проверяет поиск людей по заданным некорректным параметрам.

    Args:
        api_session: экземпляр клиентской сессии.
        admin_token: access token админа
        query_data: параметры запроса для получения ответа API.
        expected_body: ожидаемый ответ API.
        expected_status: ожидаемый статус ответа API.
    """
    url = f'{settings.service_url}/api/v1/persons/search'

    body, headers, status = await api_request(api_session, 'GET', url, params=query_data, token=admin_token)

    assert status == expected_status
    assert body == expected_body
