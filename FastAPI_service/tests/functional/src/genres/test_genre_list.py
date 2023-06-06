"""Модуль отвечает за тестирование получения списка жанров."""

import pytest

from tests.functional.settings import settings
from tests.functional.testdata.genres import get_genre_list_limit_data, get_genre_scrolling_data
from tests.functional.testdata.limits import get_test_data_for_wrong_limit
from tests.functional.utils.storages import write_data_to_es
from tests.functional.utils.api import api_request


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'wrong_limit, expected_body, expected_status',
    get_test_data_for_wrong_limit(),
)
async def test_negative_limit_genre(
    api_session,
    admin_token,
    wrong_limit,
    expected_body,
    expected_status,
):
    """
    Функция тестирует корректную обработку ошибочных значений limita для списка жанров.

    Args:
        api_session: экземпляр клиентской сессии.
        admin_token: access token админа
        wrong_limit: значение лимита.
        expected_body: ожидаемое тело ответа.
        expected_status: ожидаемый статус ответа.
    """
    url = f'{settings.service_url}/api/v1/genres/'

    body, _, status = await api_request(
        api_session,
        'GET',
        url,
        params={'limit': wrong_limit},
        token=admin_token
    )

    assert status == expected_status
    assert body == expected_body


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'query_data, test_data, expected_count_records',
    get_genre_list_limit_data(),
)
async def test_correct_limit_genre(
    es_client,
    api_session,
    admin_token,
    query_data,
    test_data,
    expected_count_records,
):
    """
    Функция тестирует корректную работу лимита для списка жанров.

    Args:
        es_client: экземпляр клиента Elasticsearch.
        api_session: экземпляр клиентской сессии.
        admin_token: access token админа
        query_data: параметры запроса к API.
        test_data: тестовые данные.
        expected_count_records: ожидаемое количество записей результата.
    """
    await write_data_to_es(es_client, settings.elastic_index.GENRES, test_data)
    url = f'{settings.service_url}/api/v1/genres/'

    body, _, status = await api_request(api_session, 'GET', url, params=query_data, token=admin_token)

    count_records = len(body.get('result', []))
    assert count_records == expected_count_records


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'test_data, limit, scroll_limit',
    get_genre_scrolling_data(),
)
async def test_scrolling(
    es_client,
    api_session,
    admin_token,
    test_data,
    limit,
    scroll_limit,
):
    """
    Тест проверяет корректную работу скроллинга для API жанров.

    Args:
        es_client: экземпляр клиента Elasticsearch.
        api_session: экземпляр клиентской сессии.
        admin_token: access token админа
        test_data: тестовые данные.
        limit: количество данных для вывода.
        scroll_limit: количество иттераций скроллинга.
    """
    await write_data_to_es(es_client, settings.elastic_index.GENRES, test_data)
    prev_search_after = None
    url = f'{settings.service_url}/api/v1/genres/'
    prev_body = {}

    for scroll_index in range(scroll_limit):
        body, _, status = await api_request(
            api_session,
            'GET',
            url,
            params={'limit': limit, 'search_after': prev_search_after},
            token=admin_token
        )
        is_scrolling_work = body != prev_body

        if not is_scrolling_work:
            assert False

        prev_search_after = body.get('outcome', {}).get('search_after', [])
        prev_body = body
        is_last_page = not prev_search_after

        if is_last_page:
            break

    assert True
