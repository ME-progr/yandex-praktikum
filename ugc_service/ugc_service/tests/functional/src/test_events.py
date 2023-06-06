"""Модуль отвечает за тестирование обработки событий."""

import pytest

from utils.api import api_request
from testdata.events import get_film_frame_data


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'film_id, film_frame, expected_status',
    get_film_frame_data(),
)
async def test_write_event(
    api_session,
    prepared_tokens,
    film_id,
    film_frame,
    expected_status
):
    """Тест для проверки записи в Kafka"""

    token = prepared_tokens.get('admin_access_token')
    query = {'film_id': film_id, 'film_frame': film_frame}
    url = '/ugc/api/v1/event/write_event'

    body, headers, status = await api_request(api_session, 'POST', url, params=query, token=token)

    assert status == expected_status
