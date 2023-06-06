"""Модуль отвечает за тестирование работы с рейтингом."""

from random import randint

import pytest

from utils.api import api_request
from testdata.film_rating import get_film_rating_data, get_film_id_data


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'film_id, rating, expected_status',
    get_film_rating_data(),
)
async def test_write_film_rating(
    api_session,
    prepared_tokens,
    film_id,
    rating,
    expected_status
):
    """Тест для проверки записи рейтинга фильма."""

    token = prepared_tokens.get('admin_access_token')
    query = {'rating': rating}
    url = f'/ugc/api/v1/film-rating/{film_id}'

    body, headers, status = await api_request(api_session, 'POST', url, json=query, token=token)

    assert status == expected_status


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'film_id, expected_status',
    get_film_id_data(),
)
async def test_get_film_user_rating(
    api_session,
    prepared_tokens,
    film_id,
    expected_status
):
    """Тест для проверки предоставления рейтинга фильма."""

    token = prepared_tokens.get('admin_access_token')
    query = {'rating': randint(1, 10)}
    url = f'/ugc/api/v1/film-rating/{film_id}'
    await api_request(api_session, 'POST', url, json=query, token=token)

    body, headers, status = await api_request(api_session, 'GET', url, token=token)

    assert status == expected_status


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'film_id, expected_status',
    get_film_id_data(),
)
async def test_update_film_user_rating(
    api_session,
    prepared_tokens,
    film_id,
    expected_status
):
    """Тест для проверки обновления рейтинга фильма."""

    token = prepared_tokens.get('admin_access_token')
    query = {'rating': randint(1, 10)}
    url = f'/ugc/api/v1/film-rating/{film_id}'
    await api_request(api_session, 'POST', url, json=query, token=token)
    query = {'rating': randint(1, 10)}

    body, headers, status = await api_request(api_session, 'PATCH', url, json=query, token=token)

    assert status == expected_status


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'film_id, expected_status',
    get_film_id_data(),
)
async def test_delete_film_user_rating(
    api_session,
    prepared_tokens,
    film_id,
    expected_status
):
    """Тест для проверки удаления рейтинга фильма."""

    token = prepared_tokens.get('admin_access_token')
    query = {'rating': randint(1, 10)}
    url = f'/ugc/api/v1/film-rating/{film_id}'
    await api_request(api_session, 'POST', url, json=query, token=token)

    body, headers, status = await api_request(api_session, 'DELETE', url, token=token)

    assert status == expected_status


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'film_id, expected_status',
    get_film_id_data(),
)
async def test_get_average_film_user_rating(
    api_session,
    prepared_tokens,
    film_id,
    expected_status
):
    """Тест для проверки предоставления среднего рейтинга фильма."""

    token = prepared_tokens.get('admin_access_token')
    url = f'/ugc/api/v1/film-rating/{film_id}'
    film_count = 3
    for i in range(film_count):
        query = {'rating': randint(1, 10)}
        await api_request(api_session, 'POST', url, json=query, token=token)
    url = f'/ugc/api/v1/film-rating/{film_id}/average'

    body, headers, status = await api_request(api_session, 'GET', url)

    assert status == expected_status
