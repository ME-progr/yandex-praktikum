"""Endpoints для жанров."""

from typing import Any

from fastapi import APIRouter, Depends, Query, Request

from models.genres import GenreBase
from models.list_base_models import GenreListResult
from models.exceptions import ExceptionResponse
from services.genres import GenreService, get_genre_service
from services.permissions.decorators import check_permissions

from docs.api_documentations import get_description_for_swagger

GENRES_DESCRIPTION, GENRE_DETAILS_DESCRIPTION = \
    get_description_for_swagger(__file__)

genres_router = APIRouter()


@genres_router.get(
    '/{genre_id}',
    response_model=GenreBase | ExceptionResponse,
    summary='Отображение информации о жанре',
    response_description='Информация о жанре',
    description=GENRE_DETAILS_DESCRIPTION
)
@check_permissions
async def genre_details(
    genre_id: str,
    genre_service: GenreService = Depends(get_genre_service),
    request: Request = Request
) -> GenreBase:
    """
    API возвращает всю информацию о конкретном жанре по `id`.

    `Args`:
        genre_id (str): идентификатор интересующего фильма

    `Returns`:
        GenreBase (pydantic-схема):
            - id (str): идентификатор жанра
            - name (str): название жанра
            - description (str): описание жанра
    """
    return await genre_service.get_genre_by_id(genre_id)


@genres_router.get(
    '/',
    response_model=GenreListResult | ExceptionResponse,
    summary='Отображение списка жанров',
    response_description='Список жанров',
    description=GENRES_DESCRIPTION
)
@check_permissions
async def genres(
    limit: int = Query(ge=1),
    search_after: list[Any] | None = Query(default=None),
    genre_service: GenreService = Depends(get_genre_service),
    request: Request = Request
) -> GenreListResult:
    """
    API возвращает список всех доступных жанров.
    Пагинация ведётся по признаку `search_after`. Для получения первой страницы этот параметр необязателен.
    Для получения следубщихих страниц нужно в `search_after` указать все значения из `outcome`
    в ответе первой и последующих страниц.

    `Args`:
        - limit (int): количество записей, которое нужно вернуть.
        - search_after (list[Any]): отправная точка, от которой идти следующая подборка
        Для получения первой страницы его не нужно передавать, далее передаем то, что вернул ответ функции.

    `Returns`:
        GenreListResult (pydantic-схема):
            - result (list): список жанров:
                - id (str): идентификатор жанра
                - name (str): название жанра
                - description (str): описание жанра
            - outcome (dict):
                - search_after (list[Any]):
                    - id (str): идентификатор жанра
    """
    return await genre_service.get_genres(limit, search_after)
