import pytest

from tests.functional.settings import settings
from tests.functional.testdata.persons import get_person_data, get_persons_data
from tests.functional.utils.cache import make_cache_id_by_template
from tests.functional.utils.storages import write_data_to_es, get_item_from_cache
from tests.functional.utils.api import api_request


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'test_data, expected_body, expected_status',
    get_person_data(),
)
async def test_cache_persons_detail(
    es_client,
    redis_client,
    api_session,
    admin_token,
    test_data,
    expected_body,
    expected_status
):
    """
    Функция тестирует работу кэша API для ручки получения детальной информации о человеке.

    Args:
        es_client: экземпляр клиента Elasticsearch.
        redis_client: экземпляр клиента Redis.
        api_session: экземпляр клиентской сессии.
        admin_token: access token админа
        test_data: тестовые данные, с которыми будем работать.
        expected_body: ожидаемый ответ API.
        expected_status: ожидаемый статус ответа API.
    """
    person_id = test_data.get('id')
    await write_data_to_es(es_client, settings.elastic_index.PERSONS, [test_data])
    url = f'{settings.service_url}/api/v1/persons/{person_id}'
    cache_id = make_cache_id_by_template(
        settings.cls_names_for_cached_id.PERSONS.value,
        settings.foo_names_for_cached_id.PERSON_ID.value,
        person_id
    )

    body, headers, status = await api_request(api_session, 'GET', url, token=admin_token)
    cache_body = await get_item_from_cache(redis_client, cache_id)

    assert status == expected_status
    assert body == expected_body == cache_body


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'query_data, test_data, expected_body, expected_status',
    get_persons_data(),
)
async def test_cache_search_persons(
    es_client,
    redis_client,
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
        redis_client: экземпляр клиента Redis.
        api_session: экземпляр клиентской сессии.
        admin_token: access token админа
        query_data: параметры запроса для получения ответа API.
        test_data: тестовые данные, с которыми будем работать.
        expected_body: ожидаемый ответ API.
        expected_status: ожидаемый статус ответа API.
    """
    await write_data_to_es(es_client, settings.elastic_index.PERSONS, test_data)
    url = f'{settings.service_url}/api/v1/persons/search'
    cache_id = make_cache_id_by_template(
        settings.cls_names_for_cached_id.PERSONS.value,
        settings.foo_names_for_cached_id.SEARCH_PERSONS.value,
        query_data.get('limit'),
        query_data.get('full_name'),
        query_data.get('search_after')
    )

    body, headers, status = await api_request(api_session, 'GET', url, params=query_data, token=admin_token)
    cache_body = await get_item_from_cache(redis_client, cache_id)

    assert status == expected_status
    assert body == cache_body
