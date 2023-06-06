"""Модуль, содержащий вспомогательные объекты для взаимодействия с внешними ресурсами."""

from http import HTTPStatus
import aiohttp
from aiohttp.client_exceptions import ClientResponseError

from ugc_service.src.models.exceptions import ExceptionResponse


async def api_request(
        api_session: aiohttp.ClientSession,
        request_method: str,
        url: str,
        params: dict | None = None,
        json: dict | None = None,
        token: str | None = None
) -> dict | ExceptionResponse:
    """Функция отвечает за запросы к API.

    Args:
        api_session: экзепляр клиентской сессии.
        request_method: метод запроса.
        url: url-адрес API.
        json: параметры запроса к API в параметрах запроса.
            Параметры со значением None фильтруются и не участвуют в запросе.
        params: параметры запроса к API в теле запроса.
            Параметры со значением None фильтруются и не участвуют в запросе.
        token: токен пользователя.
    """

    if params:
        params = {key: value for key, value in params.items() if value is not None}
    if json:
        json = {key: value for key, value in json.items() if value is not None}

    if token:
        api_session.headers.update({'Authorization': f'Bearer {token}'})
    else:
        api_session.headers.clear()

    try:
        async with api_session.request(
                request_method,
                url,
                params=params,
                json=json
        ) as response:
            body = await response.json()
            headers = response.headers
            status = response.status

    except ClientResponseError as error:
        return ExceptionResponse(msg='Переданы некорректные данные.', status_code=error.status)
    except Exception:
        return ExceptionResponse(
            msg='Что-то пошло не так. Мы уже занимаемся проблемой.',
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR
        )

    return {'body': body, 'headers': headers, 'status': status}
