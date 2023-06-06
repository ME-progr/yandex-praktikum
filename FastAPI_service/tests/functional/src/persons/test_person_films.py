import pytest

from tests.functional.settings import settings
from tests.functional.testdata.persons import generate_person_films_data, generate_incorrect_input_for_person_films
from tests.functional.utils.storages import write_data_to_es
from tests.functional.utils.api import api_request


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'query_data, test_person_data, test_films_data, expected_body, expected_status',
    generate_person_films_data(),
)
async def test_person_films(
    es_client,
    api_session,
    admin_token,
    query_data,
    test_person_data,
    test_films_data,
    expected_body,
    expected_status
):
    """
    Тест проверяет получение фильмов по id человека.

    Args:
        es_client: экземпляр клиента Elasticsearch.
        api_session: экземпляр клиентской сессии.
        admin_token: access token админа
        query_data: параметры запроса для получения ответа API.
        test_person_data: тестовые данные по человеку, с которыми будем работать.
        test_films_data: тестовые данные по фильмам, с которыми будем работать.
        expected_body: ожидаемый ответ API.
        expected_status: ожидаемый статус ответа API.
    """
    person_id = test_person_data.get('id')
    await write_data_to_es(es_client, settings.elastic_index.PERSONS, [test_person_data])
    await write_data_to_es(es_client, settings.elastic_index.MOVIES, test_films_data)
    url = f'{settings.service_url}/api/v1/persons/{person_id}/film'

    body, headers, status = await api_request(api_session, 'GET', url, params=query_data, token=admin_token)

    assert status == expected_status
    assert body == expected_body


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'query_data, expected_body, expected_status',
    generate_incorrect_input_for_person_films(),
)
async def test_incorrect_input_for_person_films(
    api_session,
    admin_token,
    query_data,
    expected_body,
    expected_status
):
    """
    Тест проверяет получение фильмов по id человека
    с некорректными входными данными в запросе.

    Args:
        api_session: экземпляр клиентской сессии.
        admin_token: access token админа
        query_data: параметры запроса для получения ответа API.
        expected_body: ожидаемый ответ API.
        expected_status: ожидаемый статус ответа API.
    """
    person_id = query_data.get('person_id')
    url = f'{settings.service_url}/api/v1/persons/{person_id}/film'

    body, headers, status = await api_request(api_session, 'GET', url, params=query_data, token=admin_token)

    assert status == expected_status
    assert body == expected_body
