"""Модуль отвечает за API отзывов к фильмам."""

from fastapi import APIRouter, Depends, Query

from ugc_service.src.models.auth_models import HTTPTokenAuthorizationCredentials
from ugc_service.src.models.body_models import ReviewBody
from ugc_service.src.models.film_review import FilmReview
from ugc_service.src.models.response_models import IdResponse, Response, FilmReviewListResponse
from ugc_service.src.services.auth_validation.bearer_tokens import JWTBearer
from ugc_service.src.services.film_review import FilmUserReviewService, get_film_user_review_service
from ugc_service.src.docs.api_documentations import (
    CREATE_FILM_USER_REVIEW_DESCRIPTION, GET_FILM_USER_REVIEW_DESCRIPTION, UPDATE_FILM_USER_REVIEW_DESCRIPTION,
    DELETE_FILM_USER_REVIEW_DESCRIPTION, GET_FILM_REVIEWS_DESCRIPTION
)

film_review_router = APIRouter()

jwt_bearer = JWTBearer()


@film_review_router.post(
    '/{film_id}',
    response_model=IdResponse,
    summary='Запись отзыва на фильм.',
    response_description='Идентификатор записи.',
    description=CREATE_FILM_USER_REVIEW_DESCRIPTION
)
async def create_film_user_review(
    film_id: str,
    body: ReviewBody,
    film_user_service: FilmUserReviewService = Depends(get_film_user_review_service),
    credentials: HTTPTokenAuthorizationCredentials = Depends(jwt_bearer),
):
    """
    Ручка позволяет пользователю оставить отзыв на конкретный фильм.

    `Args`:
        - film_id: идентификатор фильма
        - body: тело запроса
        - film_user_service: сервис для работы с пользовательскими отзывами к фильму
        - credentials: данные входа

    `Returns`:
        - IdResponse
    """
    user_id = credentials.payload.sub.user_id
    return await film_user_service.create_review(film_id, user_id, body.review)


@film_review_router.get(
    '/{film_id}',
    summary='Предоставление отзыва на фильм.',
    response_description='Отзыв на фильм.',
    description=GET_FILM_USER_REVIEW_DESCRIPTION
)
async def get_film_user_review(
    film_id: str,
    film_user_service: FilmUserReviewService = Depends(get_film_user_review_service),
    credentials: HTTPTokenAuthorizationCredentials = Depends(jwt_bearer),
) -> FilmReview | None:
    """
    Ручка получает отзыв пользователя для заданного фильма.

    `Args`:
        - film_id: идентификатор фильма
        - film_user_service: сервис для работы с пользовательским рейтингом
        - credentials: данные входа

    `Returns`:
        - ReviewResponse
    """
    user_id = credentials.payload.sub.user_id
    return await film_user_service.get_review(film_id, user_id)


@film_review_router.patch(
    '/{film_id}',
    summary='Обновление отзыва на фильм.',
    response_description='Обновлённый отзыв.',
    description=UPDATE_FILM_USER_REVIEW_DESCRIPTION
)
async def update_film_user_review(
    film_id: str,
    body: ReviewBody,
    film_user_service: FilmUserReviewService = Depends(get_film_user_review_service),
    credentials: HTTPTokenAuthorizationCredentials = Depends(jwt_bearer),
) -> FilmReview:
    """
    Ручка получает рейтинг пользователя для заданного фильма.

    `Args`:
        - film_id: идентификатор фильма
        - body: тело запроса
        - film_user_service: сервис для работы с пользовательским рейтингом
        - credentials: данные входа

    `Returns`:
        - UpdatedReview
    """
    user_id = credentials.payload.sub.user_id
    return await film_user_service.update_review(film_id, user_id, body.review)


@film_review_router.delete(
    '/{film_id}',
    response_model=Response,
    summary='Удаление отзыва на фильм.',
    response_description='Сообщение.',
    description=DELETE_FILM_USER_REVIEW_DESCRIPTION
)
async def delete_film_user_review(
    film_id: str,
    film_user_service: FilmUserReviewService = Depends(get_film_user_review_service),
    credentials: HTTPTokenAuthorizationCredentials = Depends(jwt_bearer),
) -> Response:
    """
    Ручка удаляет пользовательский отзыв для заданного фильма.

    `Args`:
        - film_id: идентификатор фильма
        - film_user_service: сервис для работы с пользовательским рейтингом
        - credentials: данные входа

    `Returns`:
        - Response
    """
    user_id = credentials.payload.sub.user_id
    await film_user_service.delete_review(film_id, user_id)
    return Response(detail='Отзыв успешно удален!')


@film_review_router.get(
    '/{film_id}/list',
    response_model=FilmReviewListResponse,
    summary='Предоставление списка пользовательских отзывов на фильм.',
    response_description='Список отзывов.',
    description=GET_FILM_REVIEWS_DESCRIPTION
)
async def get_film_reviews(
    film_id: str,
    sort: str = Query(..., regex=r'^((\+|-)?created_at)$'),
    page: int = Query(..., alias='navigation[page]', ge=1),
    limit: int = Query(..., alias='navigation[limit]', ge=1, le=50),
    film_user_service: FilmUserReviewService = Depends(get_film_user_review_service),
) -> FilmReviewListResponse:
    """
    Ручка получает список пользовательских отзывов для фильма.

    `Args`:
        - film_id: идентификатор фильма
        - sort: сортировка по полю
        - limit: количество результатов на одной странице
        - page: номер страницы
        - film_user_service: сервис для работы с пользовательским рейтингом

    `Returns`:
        - ListResponse
    """
    return await film_user_service.get_film_reviews(film_id, sort, limit, page)
