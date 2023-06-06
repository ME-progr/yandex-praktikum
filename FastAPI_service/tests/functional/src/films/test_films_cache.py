"""Модуль отвечает за тестирование хранимой информации в кэше."""

import pytest

from tests.functional.settings import settings
from tests.functional.testdata.films import get_test_data_for_film_detail, get_films_list_cache_data
from tests.functional.utils.cache import make_cache_id_by_template
from tests.functional.utils.storages import write_data_to_es, get_item_from_cache
from tests.functional.utils.api import api_request


@pytest.mark.parametrize(
    'test_data, expected_body, status',
    get_test_data_for_film_detail()
)
@pytest.mark.asyncio
async def test_film_detail_response_into_cache(
    es_client,
    redis_client,
    api_session,
    admin_token,
    test_data,
    expected_body,
    status
):
    """
    Тест проверяет корректность хранимой информации о конкретном фильме в кэше под соответствующим кэш-ключом.

    Args:
        es_client: экземпляр клиента Elasticsearch.
        redis_client: экземпляр клиента Redis.
        api_session: экземпляр клиентской сессии.
        admin_token: access token админа
        test_data: тестовые данные.
        expected_body: ожидаемый ответ API.
        status: ожидаемый статус ответа API.
    """
    film_id = test_data.get('id')
    await write_data_to_es(es_client, settings.elastic_index.MOVIES, [test_data])
    url = f"{settings.service_url}/api/v1/films/{film_id}"
    cache_id = make_cache_id_by_template(
        settings.cls_names_for_cached_id.MOVIES.value,
        settings.foo_names_for_cached_id.MOVIE_ID.value,
        film_id
    )

    body, _, status = await api_request(api_session, 'GET', url, token=admin_token)
    film_from_cache = await get_item_from_cache(redis_client, cache_id)

    assert film_from_cache == body == expected_body


@pytest.mark.parametrize(
    'query_data, test_datas',
    get_films_list_cache_data()
)
@pytest.mark.asyncio
async def test_films_list_cache(
        es_client,
        redis_client,
        api_session,
        admin_token,
        query_data,
        test_datas,
):
    """
    Тест проверяет корректность хранимой информации о фильмах в кэше под соответствующим кэш-ключом.

    Args:
        es_client: экземпляр клиента Elasticsearch.
        redis_client: экземпляр клиента Redis.
        api_session: экземпляр клиентской сессии.
        admin_token: access token админа
        query_data: параметры запроса к API.
        test_datas: тестовые данные.
    """

    await write_data_to_es(es_client, settings.elastic_index.MOVIES, test_datas)
    url = f'{settings.service_url}/api/v1/films/'
    cache_id = make_cache_id_by_template(
        settings.cls_names_for_cached_id.MOVIES.value,
        settings.foo_names_for_cached_id.LIST_MOVIES.value,
        query_data.get('sort'),
        query_data.get('limit'),
        query_data.get('genres'),
        query_data.get('persons'),
        query_data.get('search_after'),
    )

    body, *_ = await api_request(api_session, 'GET', url, params=query_data, token=admin_token)
    cache_body = await get_item_from_cache(redis_client, cache_id)

    assert body == cache_body
    assert len(body['result']) == query_data.get('limit')
