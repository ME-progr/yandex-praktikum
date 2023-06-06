"""Модуль отвечает за API рейтинговой системы фильмов."""

from fastapi import APIRouter, Depends

from ugc_service.src.models.auth_models import HTTPTokenAuthorizationCredentials
from ugc_service.src.models.body_models import RatingBody
from ugc_service.src.models.film_rating import FilmRating, AverageRating
from ugc_service.src.models.response_models import IdResponse, Response
from ugc_service.src.services.auth_validation.bearer_tokens import JWTBearer
from ugc_service.src.services.film_rating import get_film_user_rating_service, FilmUserRatingService
from ugc_service.src.docs.api_documentations import (
    SET_FILM_USER_RATING_DESCRIPTION, GET_FILM_USER_RATING_DESCRIPTION, UPDATE_FILM_USER_RATING_DESCRIPTION,
    DELETE_FILM_USER_RATING_DESCRIPTION, GET_AVERAGE_FILM_RATING_DESCRIPTION
)

film_rating_router = APIRouter()

jwt_bearer = JWTBearer()


@film_rating_router.post(
    '/{film_id}',
    response_model=IdResponse,
    summary='Запись пользовательского рейтинга на фильм.',
    response_description='Идентификатор записи.',
    description=SET_FILM_USER_RATING_DESCRIPTION
)
async def set_film_user_rating(
    film_id: str,
    body: RatingBody,
    film_user_service: FilmUserRatingService = Depends(get_film_user_rating_service),
    credentials: HTTPTokenAuthorizationCredentials = Depends(jwt_bearer),
):
    """
    Ручка присваивает пользовательский рейтинг заданному фильму.

    `Args`:
        - film_id: идентификатор фильма
        - body: тело запроса
        - film_user_service: сервис для работы с пользовательским рейтингом
        - credentials: данные входа

    `Returns`:
        - IdResponse
    """
    user_id = credentials.payload.sub.user_id
    return await film_user_service.set_rating(film_id, user_id, body.rating)


@film_rating_router.get(
    '/{film_id}',
    summary='Предоставление пользовательского рейтинга на фильм.',
    response_description='Пользовательский рейтинг фильма.',
    description=GET_FILM_USER_RATING_DESCRIPTION
)
async def get_film_user_rating(
    film_id: str,
    film_user_service: FilmUserRatingService = Depends(get_film_user_rating_service),
    credentials: HTTPTokenAuthorizationCredentials = Depends(jwt_bearer),
) -> FilmRating | None:
    """
    Ручка получает рейтинг пользователя для заданного фильма.

    `Args`:
        - film_id: идентификатор фильма
        - film_user_service: сервис для работы с пользовательским рейтингом
        - credentials: данные входа

    `Returns`:
        - FilmRating
    """
    user_id = credentials.payload.sub.user_id
    return await film_user_service.get_rating(film_id, user_id)


@film_rating_router.patch(
    '/{film_id}',
    summary='Обновление пользовательского рейтинга на фильм.',
    response_description='Запись с обновлённой информацией.',
    description=UPDATE_FILM_USER_RATING_DESCRIPTION
)
async def update_film_user_rating(
    film_id: str,
    body: RatingBody,
    film_user_service: FilmUserRatingService = Depends(get_film_user_rating_service),
    credentials: HTTPTokenAuthorizationCredentials = Depends(jwt_bearer),
) -> FilmRating:
    """
    Ручка обновляет пользовательский рейтинг для заданного фильма.

    `Args`:
        - film_id: идентификатор фильма
        - body: тело запроса
        - film_user_service: сервис для работы с пользовательским рейтингом
        - credentials: данные входа

    `Returns`:
        - UpdatedRatingResponse
    """
    user_id = credentials.payload.sub.user_id
    return await film_user_service.update_rating(film_id, user_id, body.rating)


@film_rating_router.delete(
    '/{film_id}',
    response_model=Response,
    summary='Удаление пользовательского рейтинга на фильм.',
    response_description='Сообщение.',
    description=DELETE_FILM_USER_RATING_DESCRIPTION
)
async def delete_film_user_rating(
    film_id: str,
    film_user_service: FilmUserRatingService = Depends(get_film_user_rating_service),
    credentials: HTTPTokenAuthorizationCredentials = Depends(jwt_bearer),
) -> Response:
    """
    Ручка удяляет пользовательский рейтинг для заданного фильма.

    `Args`:
        - film_id: идентификатор фильма
        - film_user_service: сервис для работы с пользовательским рейтингом
        - credentials: данные входа

    `Returns`:
        - Response
    """
    user_id = credentials.payload.sub.user_id
    await film_user_service.delete_rating(film_id, user_id)
    return Response(detail='Пользовательский рейтинг успешно удален!')


@film_rating_router.get(
    '/{film_id}/average',
    response_model=AverageRating,
    summary='Предоставление среднего пользовательского рейтинга на фильм.',
    response_description='Средний рейтинг на фильм.',
    description=GET_AVERAGE_FILM_RATING_DESCRIPTION
)
async def get_average_film_rating(
    film_id: str,
    film_user_service: FilmUserRatingService = Depends(get_film_user_rating_service),
):
    """
    Ручка получает средний пользовательский рейтинг для фильма.

    `Args`:
        - film_id: идентификатор фильма
        - film_user_service: сервис для работы с пользовательским рейтингом

    `Returns`:
        - AverageRating
    """
    return await film_user_service.get_average_rating(film_id)
