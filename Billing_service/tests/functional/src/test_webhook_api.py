"""Модуль отвечает за тестирование обработки событий."""

import pytest

from tests.functional.utils.api import api_request
from tests.functional.settings import settings


@pytest.mark.asyncio
async def test_webhook_api(
    api_session,
):
    """Тестирование доступоности ручки обработки событий, которые посылает платежная система."""

    url = f'http://{settings.billing_host}:{settings.billing_port}/billing/api/v1/webhook/'
    header_host = f'{settings.billing_header_host}:{settings.billing_port}'
    expected_body = {
        "name": "Webhook Api",
        "description": "АПИ для обработки событий, которые посылает платежная система.",
        "renders": [
            "application/json",
            "text/html"
        ],
        "parses": [
            "application/json",
            "application/x-www-form-urlencoded",
            "multipart/form-data"
        ],
        "actions": {
            "POST": {
                "type": {
                    "type": "string",
                    "required": True,
                    "read_only": False,
                    "label": "Type"
                },
                "data": {
                    "type": "field",
                    "required": True,
                    "read_only": False,
                    "label": "Data"
                }
            }
        }
    }

    body, headers, status = await api_request(api_session, 'OPTIONS', url, header_host=header_host)

    assert body == expected_body


