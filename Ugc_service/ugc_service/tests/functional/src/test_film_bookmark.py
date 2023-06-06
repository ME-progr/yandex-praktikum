"""Модуль отвечает за тестирование работы с рейтингом."""

from uuid import uuid4
from http import HTTPStatus

import pytest

from utils.api import api_request


@pytest.mark.asyncio
async def test_add_film_to_user_bookmarks(
    api_session,
    prepared_tokens,
):
    """Тест для добавления фильма в закладки."""

    token = prepared_tokens.get('admin_access_token')
    url = '/ugc/api/v1/user-bookmark'
    query = {'bookmark_film_id': str(uuid4())}

    body, headers, status = await api_request(api_session, 'POST', url, json=query, token=token)

    assert status == HTTPStatus.OK


@pytest.mark.asyncio
async def test_delete_film_from_user_bookmarks(
    api_session,
    prepared_tokens
):
    """Тест для удаления фильма из закладок."""

    film_id = str(uuid4())
    token = prepared_tokens.get('admin_access_token')
    url = '/ugc/api/v1/user-bookmark'
    query = {'bookmark_film_id': film_id}
    await api_request(api_session, 'POST', url, json=query, token=token)
    url = f'/ugc/api/v1/user-bookmark/{film_id}'

    body, headers, status = await api_request(api_session, 'DELETE', url, token=token)

    assert status == HTTPStatus.OK


@pytest.mark.asyncio
async def test_get_user_bookmarks(
    api_session,
    prepared_tokens
):
    """Тест для проверки предоставления всех закладок пользователя."""

    token = prepared_tokens.get('admin_access_token')
    url = '/ugc/api/v1/user-bookmark'
    bookmarks_count = 3
    for i in range(bookmarks_count):
        query = {'bookmark_film_id': str(uuid4())}
        await api_request(api_session, 'POST', url, json=query, token=token)
    url = '/ugc/api/v1/user-bookmark/list'
    query = {
        'sort': '-created_at',
        'navigation[page]': 1,
        'navigation[limit]': 10
    }

    body, headers, status = await api_request(api_session, 'GET', url, params=query, token=token)

    assert status == HTTPStatus.OK
