"""Модуль содержит различные тестовые данные для жанров."""

import uuid

from collections import namedtuple
from functools import lru_cache
from http import HTTPStatus


def get_genre_existed_detail_data() -> list[tuple]:
    """Функция генерирует тестовые данные для тестирования получения детальной информации о жанре."""
    TestData = namedtuple('TestData', ['test_data', 'expected_body', 'expected_status'])

    genre = _get_genres(1)[0]

    expected_body = genre.copy()
    expected_body.pop('_id')

    return [
        TestData(
            test_data=genre,
            expected_body=expected_body,
            expected_status=HTTPStatus.OK,
        ),
    ]


def get_genre_empty_detail_data() -> list[tuple]:
    """Функция генерирует тестовые данные для тестирования получения детальной информации отсутсвующего жанра."""
    TestData = namedtuple('TestData', ['test_data', 'expected_status'])
    return [
        TestData(
            test_data=str(uuid.uuid4()),
            expected_status=HTTPStatus.NOT_FOUND,
        ),
    ]


def get_genre_detail_cache_data() -> list[dict]:
    """Функция генерирует тестовые данные для теста кэша по детальной информации о фильме."""
    return _get_genres(1)


def get_genre_list_cache_data() -> list[tuple]:
    """Функция генерирует тестовые данные для тестирования получения информации по жанрам из кэша"""
    TestData = namedtuple('TestData', ['query_data', 'test_data'])
    count_genres = 20

    genres = _get_genres(count_genres)

    return [
        TestData(
            query_data={'limit': count_genres, 'search_after': None},
            test_data=genres,
        ),
    ]


def get_genre_list_limit_data() -> list[tuple]:
    """Функция генерирует тестовые данные для тестирования корректной работы лимита."""
    TestData = namedtuple('TestData', ['query_data', 'test_data', 'expected_count_records'])
    list_count_genres = (20, 40, 80)

    result = []

    for count_genres in list_count_genres:
        result.append(TestData(
            query_data={'limit': count_genres, 'search_after': None},
            test_data=_get_genres(count_genres),
            expected_count_records=count_genres
        ))

    return result


def get_genre_scrolling_data() -> list[tuple]:
    """Функция генерирует тестовые данные для тестирования корректной работы скролла."""
    TestData = namedtuple('TestData', ['test_data', 'limit', 'scroll_limit'])
    return [
        TestData(
            test_data=_get_genres(80),
            limit=20,
            scroll_limit=1,
        ),
        TestData(
            test_data=_get_genres(80),
            limit=20,
            scroll_limit=3,
        ),
        TestData(
            test_data=_get_genres(80),
            limit=20,
            scroll_limit=4,
        ),
        TestData(
            test_data=_get_genres(80),
            limit=20,
            scroll_limit=5,
        ),
        TestData(
            test_data=_get_genres(80),
            limit=30,
            scroll_limit=4,
        ),
    ]


@lru_cache
def _get_genres(count_genres: int) -> list[dict]:
    """
    Функция генерирует список жанров по заданному количеству.

    Args:
        count_genres: количество жанров.
    """
    genres = []

    for index in range(count_genres):
        genre_id = str(uuid.uuid4())
        genres.append({
            '_id': genre_id,
            'id': genre_id,
            'name': f'Test genre {index}',
            'description': f'Test genre {index}',
        })

    return genres
