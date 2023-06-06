"""Модуль отвечает за API событий."""

from http import HTTPStatus

from fastapi import APIRouter, Depends

from ugc_service.src.core.config import TopicName
from ugc_service.src.models.auth_models import HTTPTokenAuthorizationCredentials
from ugc_service.src.services.auth_validation.bearer_tokens import JWTBearer
from ugc_service.src.services.events import get_event_service, EventService
from ugc_service.src.docs.api_documentations import WRITE_FILM_FRAME_DESCRIPTION

event_router = APIRouter()

jwt_bearer = JWTBearer()


@event_router.post(
    '/write_event',
    summary='Запись времени фильма определённого пользователя',
    response_description='Статус',
    description=WRITE_FILM_FRAME_DESCRIPTION
)
async def write_film_frame(
    film_id: str,
    film_frame: str,
    event_service: EventService = Depends(get_event_service),
    credentials: HTTPTokenAuthorizationCredentials = Depends(jwt_bearer),
):
    """
    Ручка сохраняет момент, на котором в данный момент находится пользователь при просмотре фильма.

    `Args`:
        - film_id: идентификатор фильма
        - film_frame: момент, на котором остановился пользователь
        - event_service: сервис работы с событиями
        - credentials: данные входа
    `Returns`:
        - HTTPStatus
    """
    user_id = credentials.payload.sub.user_id
    topic = TopicName.FRAMERATE.value
    key = f'{user_id}+{film_id}'

    await event_service.write_event(topic=topic, key=key, value=film_frame)

    return HTTPStatus.OK
