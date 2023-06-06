"""Модуль по тестированию списков у API фильмов."""

import re

import pytest

from tests.functional.settings import settings
from tests.functional.testdata.films import get_test_films_title, get_films_scrolling_data
from tests.functional.utils.storages import write_data_to_es
from tests.functional.utils.api import api_request


@pytest.mark.parametrize(
    'query_data, test_datas',
    get_test_films_title()
)
@pytest.mark.asyncio
async def test_search_films(
    es_client,
    api_session,
    admin_token,
    query_data,
    test_datas
):
    """
    Тест проверяет получение фильмов через поиск.

    Args:
        es_client: экземпляр клиента Elasticsearch.
        api_session: экземпляр клиентской сессии.
        admin_token: access token админа
        query_data: параметры запроса к API.
        test_datas: тестовые данные, с которыми будем работать.
    """

    await write_data_to_es(es_client, settings.elastic_index.MOVIES, test_datas)
    url = f'{settings.service_url}/api/v1/films/search/'

    body, *_ = await api_request(api_session, 'GET', url, params=query_data, token=admin_token)

    for film in body.get('result'):
        assert True if re.search(query_data.get('title'), film.get('title')) else False


@pytest.mark.asyncio
async def test_response_for_wrong_sort(
    api_session,
    admin_token
):
    """
    Тест проверяет корректность ответа при невалидных параметрах сортировки.

    Args:
        api_session: экземпляр клиентской сессии.
        admin_token: access token админа
    """
    error_msg = {
        'detail': [
            {
                'ctx': {
                    'pattern': '^(-?imdb_rating|-?title)$'
                },
                'loc': ['query', 'sort'],
                'msg': 'string does not match regex "^(-?imdb_rating|-?title)$"',
                'type': 'value_error.str.regex'
            }
        ]
    }
    url = f'{settings.service_url}/api/v1/films/'

    body, *_ = await api_request(
        api_session,
        'GET',
        url,
        params={'sort': 'persons', 'limit': 20},
        token=admin_token
    )

    assert body == error_msg


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'test_data, limit, scroll_limit',
    get_films_scrolling_data(),
)
async def test_films_scrolling(
    es_client,
    api_session,
    admin_token,
    test_data,
    limit,
    scroll_limit,
):
    """
    Тест проверяет корректную работу скроллинга для API фильмов.

    Args:
        es_client: экземпляр клиента Elasticsearch.
        api_session: экземпляр клиентской сессии.
        admin_token: access token админа
        test_data: тестовые данные.
        limit: количество данных для вывода.
        scroll_limit: количество итераций скроллинга.
    """

    await write_data_to_es(es_client, settings.elastic_index.MOVIES, test_data)
    url = f'{settings.service_url}/api/v1/films/'
    prev_body, prev_search_after = {}, None

    for scroll_index in range(scroll_limit):
        body, *_ = await api_request(
            api_session,
            'GET',
            url,
            params={
                'sort': '-imdb_rating',
                'limit': limit,
                'search_after': prev_search_after
            },
            token=admin_token
        )
        is_scrolling_work = body != prev_body

        if not is_scrolling_work:
            assert False

        prev_search_after = body.get('outcome').get('search_after')
        prev_body = body

        if not prev_search_after:
            break

    assert True
