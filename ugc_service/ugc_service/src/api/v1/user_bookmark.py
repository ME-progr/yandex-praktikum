"""Модуль отвечает за API для закладок пользователя."""

from fastapi import APIRouter, Depends, Query

from ugc_service.src.models.auth_models import HTTPTokenAuthorizationCredentials
from ugc_service.src.models.body_models import FilmBookmarkBody
from ugc_service.src.models.response_models import IdResponse, UserBookmarkListResponse, Response
from ugc_service.src.services.auth_validation.bearer_tokens import JWTBearer
from ugc_service.src.services.user_bookmark import UserBookmarkService, get_user_bookmark_service
from ugc_service.src.docs.api_documentations import (
    ADD_FILM_TO_USER_BOOKMARKS_DESCRIPTION, DELETE_FILM_FROM_USER_BOOKMARKS_DESCRIPTION, GET_USER_BOOKMARKS_DESCRIPTION
)

user_bookmark_router = APIRouter()

jwt_bearer = JWTBearer()


@user_bookmark_router.post(
    '/',
    response_model=IdResponse,
    summary='Добавление фильма в закладки пользователя.',
    response_description='Идентификатор записи.',
    description=ADD_FILM_TO_USER_BOOKMARKS_DESCRIPTION
)
async def add_film_to_user_bookmarks(
    body: FilmBookmarkBody,
    user_bookmark_service: UserBookmarkService = Depends(get_user_bookmark_service),
    credentials: HTTPTokenAuthorizationCredentials = Depends(jwt_bearer),
):
    """
    Ручка позволяет пользователю добавить фильм в закладки.

    `Args`:
        - body: тело запроса
        - user_bookmark_service: сервис для работы с пользовательскими закладками
        - credentials: данные входа

    `Returns`:
        - IdResponse
    """
    user_id = credentials.payload.sub.user_id
    return await user_bookmark_service.add_film_to_user_bookmarks(body.bookmark_film_id, user_id)


@user_bookmark_router.delete(
    '/{film_id}',
    response_model=Response,
    summary='Удаление фильма из закладок пользователя.',
    response_description='Сообщений.',
    description=DELETE_FILM_FROM_USER_BOOKMARKS_DESCRIPTION
)
async def delete_film_from_user_bookmarks(
    film_id: str,
    user_bookmark_service: UserBookmarkService = Depends(get_user_bookmark_service),
    credentials: HTTPTokenAuthorizationCredentials = Depends(jwt_bearer),
):
    """
    Ручка позволяет пользователю удалить фильм из закладок.

    `Args`:
        - film_id: идентификатор фильма
        - user_bookmark_service: сервис для работы с пользовательскими закладками
        - credentials: данные входа

    `Returns`:
        - Response
    """
    user_id = credentials.payload.sub.user_id
    await user_bookmark_service.delete_film_from_user_bookmarks(film_id, user_id)
    return Response(detail='Закладка успешно удалена!')


@user_bookmark_router.get(
    '/list',
    response_model=UserBookmarkListResponse,
    summary='Предоставление всех закладок пользователя.',
    response_description='Список закладок.',
    description=GET_USER_BOOKMARKS_DESCRIPTION
)
async def get_user_bookmarks(
    sort: str = Query(..., regex=r'^((\+|-)?created_at)$'),
    page: int = Query(..., alias='navigation[page]', ge=1),
    limit: int = Query(..., alias='navigation[limit]', ge=1, le=50),
    user_bookmark_service: UserBookmarkService = Depends(get_user_bookmark_service),
    credentials: HTTPTokenAuthorizationCredentials = Depends(jwt_bearer),
) -> UserBookmarkListResponse:
    """
    Ручка получает список пользовательских закладок.

    `Args`:
        - sort: сортировка по полю
        - limit: количество результатов на одной странице
        - page: номер страницы
        - user_bookmark_service: сервис для работы с пользовательским рейтингом
        - credentials: данные входа

    `Returns`:
        - UserBookmarkListResponse
    """
    user_id = credentials.payload.sub.user_id
    return await user_bookmark_service.get_user_bookmarks(user_id, sort, limit, page)
