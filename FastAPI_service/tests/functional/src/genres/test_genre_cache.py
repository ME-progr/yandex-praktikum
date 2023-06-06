"""Модуль отвечает за тестирование детальной информации о жанрах."""

import pytest

from tests.functional.settings import settings
from tests.functional.testdata.genres import get_genre_detail_cache_data, get_genre_list_cache_data
from tests.functional.utils.cache import make_cache_id_by_template
from tests.functional.utils.storages import write_data_to_es, get_item_from_cache
from tests.functional.utils.api import api_request


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'test_data',
    get_genre_detail_cache_data(),
)
async def test_cache_genre_detail(
    es_client,
    redis_client,
    api_session,
    admin_token,
    test_data,
):
    """
    Функция тестирует работу кэша API для ручки получения детальной информации о жанре.

    Args:
        es_client: экземпляр клиента Elasticsearch.
        redis_client: экземпляр клиента Redis.
        api_session: экземпляр клиентской сессии.
        admin_token: access token админа
        test_data: тестовые данные.
    """
    genre_id = test_data.get('id')
    await write_data_to_es(es_client, settings.elastic_index.GENRES, [test_data])
    url = f'{settings.service_url}/api/v1/genres/{genre_id}'
    cache_id = make_cache_id_by_template(
        settings.cls_names_for_cached_id.GENRES.value,
        settings.foo_names_for_cached_id.GENRE_ID.value,
        genre_id,
    )

    body, _, status = await api_request(api_session, 'GET', url, token=admin_token)
    cache_body = await get_item_from_cache(redis_client, cache_id)

    assert body == cache_body


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'query_data, test_data',
    get_genre_list_cache_data(),
)
async def test_cache_genre_list(
    es_client,
    redis_client,
    api_session,
    admin_token,
    query_data,
    test_data,
):
    """
    Функция тестирует работу кэша API для ручки получения списка жанров.

    Args:
        es_client: экземпляр клиента Elasticsearch.
        redis_client: экземпляр клиента Redis.
        api_session: экземпляр клиентской сессии.
        admin_token: access token админа
        query_data: параметры запроса к API.
        test_data: тестовые данные.
    """

    await write_data_to_es(es_client, settings.elastic_index.GENRES, test_data)
    url = f'{settings.service_url}/api/v1/genres/'
    cache_id = make_cache_id_by_template(
        settings.cls_names_for_cached_id.GENRES.value,
        settings.foo_names_for_cached_id.LIST_GENRES.value,
        query_data.get('limit'),
        query_data.get('search_after'),
    )

    body, _, status = await api_request(api_session, 'GET', url, params=query_data, token=admin_token)
    cache_body = await get_item_from_cache(redis_client, cache_id)

    assert body == cache_body
    assert len(body.get('result')) == len(cache_body.get('result')) == query_data.get('limit')
