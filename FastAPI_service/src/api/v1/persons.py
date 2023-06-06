"""Endpoints для людей."""

from typing import Any

from fastapi import APIRouter, Depends, Query, Request

from models.persons import Person
from models.list_base_models import PersonListResult, FilmListResult
from models.exceptions import ExceptionResponse
from services.persons import PersonService, get_person_service
from services.films import FilmService, get_film_service
from services.permissions.decorators import check_permissions

from docs.api_documentations import get_description_for_swagger

PERSON_FILMS_DESCRIPTION, PERSON_DETAILS_DESCRIPTION, SEARCH_PERSONS_DESCRIPTION = \
    get_description_for_swagger(__file__)

persons_router = APIRouter()


@persons_router.get(
    '/search',
    response_model=PersonListResult | ExceptionResponse,
    summary='Поиск людей по имени',
    response_description='Список людей',
    description=SEARCH_PERSONS_DESCRIPTION
)
@check_permissions
async def search_persons(
        full_name: str,
        limit: int = Query(ge=1),
        search_after: list[Any] | None = Query(default=None),
        person_service: PersonService = Depends(get_person_service),
        request: Request = Request
) -> PersonListResult:
    """
    API возвращает найденную информацию о людях по имени.
    Для получения следубщихих страниц нужно в `search_after` указать все значения из `outcome`
    в ответе первой и последующих страниц.

    `Args`:
        - limit (int): кол-во людей на страницу
        - full_name (str): имя человека для поиска
        - search_after (list[Any]): отправная точка, от которой идёт следующий поиск

    `Returns`:
        PersonListResult (pydantic-схема):
            - result (list): список людей:
                - id (str): идентификатор человека
                - full_name (str): имя человека
                - roles (pydantic-схема): роли человека:
                    - actor (list[UUID]):
                        - id (str): идентификатор фильма, в котором данный человек является актёром
                    - writer (list[UUID]):
                        - id (str): идентификатор фильма, в котором данный человек является сценаристом
                    - director (list[UUID]):
                        - id (str): идентификатор фильма, в котором данный человек является режиссёром
                    - other (list[UUID]):
                        - id (str): идентификатор фильма, в котором у данного человека прочая роль
                - films (list[UUID]): список всех фильмов с участием чловека:
                    - id (str): идентификатор фильма
            - outcome (dict):
                - search_after (list[Any]):
                    - full_name (str): имя человека
                    - id (str): идентификатор человека
    """
    return await person_service.get_persons_by_searching(limit, full_name, search_after)


@persons_router.get(
    '/{person_id}',
    response_model=Person | ExceptionResponse,
    summary='Отображение детальной информации о человеке',
    response_description='Информация о человеке',
    description=PERSON_DETAILS_DESCRIPTION
)
@check_permissions
async def person_details(
        person_id: str,
        person_service: PersonService = Depends(get_person_service),
        request: Request = Request
) -> Person:
    """
    API возвращает всю информацию о конкретном человеке по `id`.

    `Args`:
        person_id (uuid): идентификатор интересующего человека

    `Returns`:
        Person (pydantic-схема):
            - id (str): идентификатор человека
            - full_name (str): имя человека
            - roles (pydantic-схема): роли человека:
                - actor (list[UUID]):
                    - id (str): идентификатор фильма, в котором данный человек является актёром
                - writer (list[UUID]):
                    - id (str): идентификатор фильма, в котором данный человек является сценаристом
                - director (list[UUID]):
                    - id (str): идентификатор фильма, в котором данный человек является режиссёром
                - other (list[UUID]):
                    - id (str): идентификатор фильма, в котором у данного человека прочая роль
            - films (list[UUID]): список всех фильмов с участием чловека:
                - id (str): идентификатор фильма
    """
    return await person_service.get_person_by_id(person_id)


@persons_router.get(
    '/{person_id}/film',
    response_model=FilmListResult | ExceptionResponse,
    summary='Поиск фильмов, в которых участвовал человек',
    response_description='Список фильмов',
    description=PERSON_FILMS_DESCRIPTION
)
@check_permissions
async def person_films(
        person_id: str,
        limit: int = Query(ge=1),
        search_after: list[Any] | None = Query(default=None),
        film_service: FilmService = Depends(get_film_service),
        request: Request = Request
) -> FilmListResult:
    """
    API возвращает информацию по фильмам, в которых участвовал человек
    Для получения сл-их страниц нужно в `search_after` указать значения из `outcome` в ответе первой и последующих стр.

    `Args`:
        - person_id (str): Идентификатор человека
        - limit (int): количество фильмов в выборке
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
    return await film_service.get_films('-imdb_rating', limit, search_after, persons=[person_id])
