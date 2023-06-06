"""Модуль с тестовыми данными для фильмов."""

import random
from collections import namedtuple
from functools import lru_cache
from http import HTTPStatus
from typing import Any
from uuid import uuid4


def get_test_films_title():
    """Функция возвращает тестовые данные для теста о получении фильмов по названию."""
    TestFilmTitle = namedtuple('TestFilmTitle', ['query_data', 'test_datas'])
    film_tile, limit = 'Star', 20

    return [
        TestFilmTitle(
            query_data={'title': film_tile, 'limit': limit},
            test_datas=_make_film_template(limit)
        )
    ]


def get_test_data_for_film_detail():
    """Функция возвращает тестовые данные для теста о получении детальной информации о фильме."""
    TestFilmDetail = namedtuple('TestFilmDetail', ['test_data', 'expected_body', 'expected_status'])

    film_detail = _make_film_template(1)[0]

    expected_body = film_detail.copy()
    expected_body.pop('_id')

    return [
        TestFilmDetail(
            test_data=film_detail,
            expected_body=expected_body,
            expected_status=HTTPStatus.OK
        )
    ]


def get_status_for_not_exist_film():
    """Функция возвращает тестовые данные для теста о получении детальной информации отсутствующего фильма."""
    FakeFilm = namedtuple('FakeFilm', ['wrong_id', 'expected_status'])
    return [
        FakeFilm(
            wrong_id=str(uuid4()),
            expected_status=HTTPStatus.NOT_FOUND
        )
    ]


def get_films_list_cache_data() -> list[tuple]:
    """Функция возвращает тестовые данные для теста о получении информации о фильмах."""
    Films = namedtuple('Films', ['query_data', 'test_datas'])
    count_films = 20

    return [
        Films(
            query_data={
                'sort': '-imdb_rating',
                'limit': count_films,

            },
            test_datas=_make_film_template(count_films),
        ),
        Films(
            query_data={
                'sort': 'title',
                'limit': count_films,

            },
            test_datas=_make_film_template(count_films, title=True),
        ),
    ]


def get_films_scrolling_data() -> list[tuple]:
    """Функция генерирует тестовые данные для тестирования корректной работы скролла."""
    TestData = namedtuple('TestData', ['test_data', 'limit', 'scroll_limit'])
    return [
        TestData(
            test_data=_make_film_template(80),
            limit=20,
            scroll_limit=4,
        ),
    ]


@lru_cache
def _make_film_template(count: int, title: bool | None = None) -> list[dict[str, Any]]:
    """
    Функция возвращает словарь, для создания документа в `ElasticSearch`.

    Args:
        count: кол-во фильмов
        title: название фильма

    Returns:
        список с информацией о фильме
    """
    films = []

    for item in range(count):

        film_id = str(uuid4())
        title = f'Test Film №{item}' if title else 'Star Wars: Episode IV - A New Hope'
        rating = round(random.uniform(0.0, 10.0), 2)

        film_detail = {
            "_id": film_id,
            "id": film_id,
            "imdb_rating": rating,
            "genres": [
                {
                    "id": "3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff",
                    "name": "Action"
                }
            ],
            "title": title,
            "description": "The Imperial Forces, under orders from cruel Darth Vader, hold Princess Leia hostage in ...",
            "actors": [],
            "writers": [],
            "directors": []
        }

        films.append(film_detail)

    return films
