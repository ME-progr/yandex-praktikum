import pytest

from tests.functional.settings import settings
from tests.functional.testdata.persons import get_person_data, generate_incorrect_input_for_persons_detail
from tests.functional.utils.storages import write_data_to_es
from tests.functional.utils.api import api_request


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'test_data, expected_body, expected_status',
    get_person_data(),
)
async def test_persons_detail(
    es_client,
    api_session,
    admin_token,
    test_data,
    expected_body,
    expected_status
):
    """
    Тест проверяет получение детальной информации о человеке.

    Args:
        es_client: экземпляр клиента Elasticsearch.
        api_session: экземпляр клиентской сессии.
        admin_token: access token админа
        test_data: тестовые данные, с которыми будем работать.
        expected_body: ожидаемый ответ API.
        expected_status: ожидаемый статус ответа API.
    """
    person_id = test_data.get('id')
    await write_data_to_es(es_client, settings.elastic_index.PERSONS, [test_data])
    url = f'{settings.service_url}/api/v1/persons/{person_id}'

    body, headers, status = await api_request(api_session, 'GET', url, token=admin_token)

    assert status == expected_status
    assert body == expected_body


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'test_data, expected_status',
    generate_incorrect_input_for_persons_detail(),
)
async def test_incorrect_input_for_persons_detail(
        api_session,
        admin_token,
        test_data,
        expected_status
):
    """
    Тест проверяет получение ошибки при некорректных входных данных
    для получения детальной информации о человеке.

    Args:
        api_session: экземпляр клиентской сессии.
        admin_token: access token админа
        test_data: тестовые данные, с которыми будем работать.
        expected_status: ожидаемый статус ответа API.
    """
    person_id = test_data
    url = f'{settings.service_url}/api/v1/persons/{person_id}'

    body, headers, status = await api_request(api_session, 'GET', url, token=admin_token)

    assert status == expected_status
