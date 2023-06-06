"""Модуль отвечает за тестирование работы с рейтингом."""

import pytest

from utils.api import api_request
from testdata.film_review import get_film_review_data, get_film_id_data


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'film_id, review, expected_status',
    get_film_review_data(),
)
async def test_create_film_review(
    api_session,
    prepared_tokens,
    film_id,
    review,
    expected_status
):
    """Тест для проверки записи отзыва на фильм."""

    token = prepared_tokens.get('admin_access_token')
    query = {'review': review}
    url = f'/ugc/api/v1/film-review/{film_id}'

    body, headers, status = await api_request(api_session, 'POST', url, json=query, token=token)

    assert status == expected_status


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'film_id, expected_status',
    get_film_id_data(),
)
async def test_get_film_user_review(
    api_session,
    prepared_tokens,
    film_id,
    expected_status
):
    """Тест для проверки предоставления отзыва на фильм."""

    token = prepared_tokens.get('admin_access_token')
    query = {'review': 'test_review'}
    url = f'/ugc/api/v1/film-review/{film_id}'
    await api_request(api_session, 'POST', url, json=query, token=token)

    body, headers, status = await api_request(api_session, 'GET', url, token=token)

    assert status == expected_status


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'film_id, expected_status',
    get_film_id_data(),
)
async def test_update_film_user_review(
    api_session,
    prepared_tokens,
    film_id,
    expected_status
):
    """Тест для проверки обновления отзыва на фильм."""

    token = prepared_tokens.get('admin_access_token')
    query = {'review': 'test_review'}
    url = f'/ugc/api/v1/film-review/{film_id}'
    await api_request(api_session, 'POST', url, json=query, token=token)
    query = {'review': 'new_test_review'}

    body, headers, status = await api_request(api_session, 'PATCH', url, json=query, token=token)

    assert status == expected_status


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'film_id, expected_status',
    get_film_id_data(),
)
async def test_delete_film_user_review(
    api_session,
    prepared_tokens,
    film_id,
    expected_status
):
    """Тест для проверки удаления отзыва на фильм."""

    token = prepared_tokens.get('admin_access_token')
    query = {'review': 'test_review'}
    url = f'/ugc/api/v1/film-review/{film_id}'
    await api_request(api_session, 'POST', url, json=query, token=token)

    body, headers, status = await api_request(api_session, 'DELETE', url, token=token)

    assert status == expected_status


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'film_id, expected_status',
    get_film_id_data(),
)
async def test_get_average_film_user_review(
    api_session,
    prepared_tokens,
    film_id,
    expected_status
):
    """Тест для проверки предоставления всех отзывов на фильма."""

    token = prepared_tokens.get('admin_access_token')
    url = f'/ugc/api/v1/film-review/{film_id}'
    film_count = 3
    for i in range(film_count):
        query = {'review': f'test_review_{i}'}
        await api_request(api_session, 'POST', url, json=query, token=token)
    url = f'/ugc/api/v1/film-review/{film_id}/list'
    query = {
        'sort': '-created_at',
        'navigation[page]': 1,
        'navigation[limit]': 10
    }

    body, headers, status = await api_request(api_session, 'GET', url, params=query)

    assert status == expected_status
