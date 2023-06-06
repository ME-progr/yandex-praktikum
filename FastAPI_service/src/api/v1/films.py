"""Endpoints для фильмов."""

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request

from models.films import Film
from models.list_base_models import FilmListResult
from models.exceptions import ExceptionResponse
from services.films import FilmService, get_film_service
from services.permissions.decorators import check_permissions

from docs.api_documentations import get_description_for_swagger

FILM_DESCRIPTION, FILM_DETAILS_DESCRIPTION, SEARCH_FILM_DESCRIPTION = \
    get_description_for_swagger(__file__)

films_router = APIRouter()


@films_router.get(
    '/search',
    response_model=FilmListResult | ExceptionResponse,
    summary='Поиск фильмов по названию',
    response_description='Найденные фильмы',
    description=SEARCH_FILM_DESCRIPTION
)
@check_permissions
async def search_films(
        title: str,
        limit: int = Query(ge=1),
        search_after: list[Any] | None = Query(default=None),
        film_service: FilmService = Depends(get_film_service),
        request: Request = Request
) -> FilmListResult:
    """
    API возвращает найденные фильмы по названию.
    Пагинация ведётся по признаку `search_after`.
    Для получения первой страницы этот параметр необязателен.
    Для получения следубщихих страниц нужно в `search_after` указать все значения из `outcome`
    в ответе первой и последующих страниц.

    `Args`:
        - limit (int): кол-во фильмов на страницу
        - title (str): название фильма для поиска
        - search_after (list[Any]): отправная точка, от которой идёт следующий поиск

    `Returns`:
        FilmListResult (pydantic-схема):
            - result (list): список фильмов:
                - id (str): идентификатор фильма
                - title (str): название фильма
                - imdb_rating (float): рейтинг фильма
            - outcome (dict):
                - search_after (list[Any]):
                    - imdb_rating (float): рейтинг фильма
                    - title (str): название фильма
    """
    return await film_service.get_films_by_searching(limit, title, search_after)


@films_router.get(
    '/{film_id}',
    response_model=Film | ExceptionResponse,
    summary='Отображение всей информации о конкретном фильме',
    response_description='Вся информация о фильме',
    description=FILM_DETAILS_DESCRIPTION
)
@check_permissions
async def film_details(
        film_id: str,
        film_service: FilmService = Depends(get_film_service),
        request: Request = Request
) -> Film:
    """
    API возвращает всю информацию о конкретном фильм по `id`.

    `Args`:
        - film_id (uuid): идентификатор интересующего фильма

    `Returns`:
        Film (pydantic-схема):
            - id (str): идентификатор фильма
            - title (str): название фильма
            - imdb_rating (float): рейтинг фильма
            - description (str)
            - genres: (list):
                - id (str): идентификатор жанра
                - name (str): название жанра
                - description (str): описание жанра
            - actors: (list):
                - id (str): идентификатор актёра
                - name (str): имя актёра
            - writers: (list):
                - id (str): идентификатор сценариста
                - name (str): имя сценариста
            - directors: (list):
                - id (str): идентификатор режиссёра
                - name (str): имя режиссёра
    """
    return await film_service.get_film_by_id(film_id)


@films_router.get(
    '/',
    response_model=FilmListResult | ExceptionResponse,
    summary='Отображение фильмов для главной страницы',
    response_description='Фильмы для главной страницы',
    description=FILM_DESCRIPTION
)
@check_permissions
async def get_films(
        sort: str = Query(..., regex=r'^(-?imdb_rating|-?title)$'),
        limit: int = Query(ge=1),
        search_after: list[Any] | None = Query(default=None),
        genres: list[UUID] | None = Query(default=None),
        persons: list[UUID] | None = Query(default=None),
        film_service: FilmService = Depends(get_film_service),
        request: Request = Request
) -> FilmListResult:
    """
    API возвращает фильмы для главной страницы.

    API поддерживает:
        - сортировку как рейтингу, так и по названию фильма (`sort`);
        - ограничение кол-ва выводимых фильмов на страницу (`limit`);
        - поиск отдельно как по жанрам (`genres`), так и по персонажам (`persons`).
        Поиск одновременно поддерживается ТОЛЬКО по одному из параметров.
        - пагинацию, ведущуюся по признаку `search_after`. Для получения первой страницы этот параметр необязателен.

    Для получения следубщихих страниц нужно в `search_after` указать все значения из `outcome`
    в ответе первой и последующих страниц.

    `Args`:
        sort (str): параметр, по которому будет идти выборка для показа на главной странице
        limit (int): кол-во фильмов на странице
        search_after (list[Any]): отправная точка, от которой идти следующая подборка
        genres (list[UUID]): интересующие жанры для выборки
        persons (list[UUID]): интересующие персонажи для выборки

    `Returns`:
        FilmListResult (pydantic-схема):
            - result (list): список фильмов:
                - id (str): идентификатор фильма
                - title (str): название фильма
                - imdb_rating (float): рейтинг фильма
            - outcome (dict):
                - search_after (list[Any]):
                    - imdb_rating (float): рейтинг фильма
                    - title (str): название фильма
    """
    return await film_service.get_films(sort, limit, search_after, genres, persons)
