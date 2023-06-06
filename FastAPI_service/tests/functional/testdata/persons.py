"""Модуль содержит различные тестовые данные для персон."""

from typing import Any

import uuid
from functools import lru_cache
from collections import namedtuple
from http import HTTPStatus


def get_person_data() -> list:
    """Функция генерирует тестовые данные для тестирования получения детальной информации о человеке."""
    TestData = namedtuple('TestData', ['test_data', 'expected_body', 'expected_status'])

    test_data, expected_body = _generate_persons_data(1)

    return [
        TestData(
            test_data=test_data[0],
            expected_body=expected_body[0],
            expected_status=HTTPStatus.OK
        )
    ]


def get_persons_data() -> list:
    """Функция генерирует тестовые данные для тестирования получения информации о людях."""
    TestData = namedtuple('TestData', ['query_data', 'test_data', 'expected_body', 'expected_status'])
    persons_count = 20
    test_data, expected_body = _generate_persons_data(persons_count)
    test_data = test_data
    expected_body = expected_body

    return [
        TestData(
            query_data={
                'full_name': 'Test person',
                'limit': persons_count,
                'search_after': None
            },
            test_data=test_data,
            expected_body=expected_body,
            expected_status=HTTPStatus.OK
        )
    ]


def generate_person_films_data() -> list:
    """Функция генерирует тестовые данные для тестирования получения фильмов по id человека."""
    TestData = namedtuple('TestData', ['query_data',
                                       'test_person_data',
                                       'test_films_data',
                                       'expected_body',
                                       'expected_status'])
    person_id = str(uuid.uuid4())

    test_person_data = {
        "_id": person_id,
        'id': person_id,
        'full_name': 'Test person',
        'actor': [],
        'director': [],
        'writer': [],
        'other': [],
        'films': []
    }

    films_count = 10
    test_films_data = []
    expected_body = {'result': []}

    for index in range(films_count):
        film_id = str(uuid.uuid4())
        title = f'Test film {index}'
        imdb_rating = 9.9

        writers_ids = [str(uuid.uuid4()), str(uuid.uuid4())]
        actors_ids = [str(uuid.uuid4()), str(uuid.uuid4())]
        directors_ids = [str(uuid.uuid4()), str(uuid.uuid4())]

        if index < 3:
            writers_ids.append(person_id)
            test_person_data['writer'].append(film_id)
        elif 3 < index < 7:
            actors_ids.append(person_id)
            test_person_data['actor'].append(film_id)
        else:
            directors_ids.append(person_id)
            test_person_data['director'].append(film_id)
        test_person_data['films'].append(film_id)

        test_films_data.append({
            '_id': film_id,
            'id': film_id,
            'imdb_rating': imdb_rating,
            'genres': [
                {
                    'id': str(uuid.uuid4()),
                    'name': 'Test genre'
                }
            ],
            'title': title,
            'description': 'Test description',
            "persons": writers_ids + actors_ids + directors_ids,
            "directors_names": ["Test director"] * len(directors_ids),
            "actors_names": ["Test actor"] * len(actors_ids),
            "writers_names": ["Test writer"] * len(writers_ids),
            "actors": [
                {
                    'id': actor_id,
                    'name': 'Test actor'
                } for actor_id in actors_ids
            ],
            "writers": [
                {
                    'id': writer_id,
                    'name': 'Test writer'
                } for writer_id in writers_ids
            ],
            "directors": [
                {
                    'id': director_id,
                    'name': 'Test director'
                } for director_id in directors_ids
            ]
        })

        expected_body['result'].append({
                    "id": film_id,
                    "title": title,
                    "imdb_rating": imdb_rating
                })

    expected_body['outcome'] = {'search_after': [9.9, f'Test film {films_count - 1}']}

    return [
        TestData(
            query_data={
                'person_id': person_id,
                'limit': films_count,
                'search_after': None
            },
            test_person_data=test_person_data,
            test_films_data=test_films_data,
            expected_body=expected_body,
            expected_status=HTTPStatus.OK
        )
    ]


def generate_incorrect_input_for_persons_detail() -> list:
    """
    Функция генерирует тестовые данные для тестирования получения ошибки
    при некорректных входных данных для получения детальной информации о человеке.
    """
    TestData = namedtuple('TestData', ['test_data', 'expected_status'])

    return [
        TestData(
            test_data=str(uuid.uuid4()),
            expected_status=HTTPStatus.NOT_FOUND
        ),
        TestData(
            test_data='',
            expected_status=HTTPStatus.NOT_FOUND
        )
    ]


def generate_incorrect_input_for_person_films():
    """
    Функция генерирует некорректные входные данные
    для тестирования получения фильмов по id человека.
    """
    TestData = namedtuple('TestData', ['query_data', 'expected_body', 'expected_status'])
    person_id = str(uuid.uuid4())
    return [
        TestData(
            query_data={
                'person_id': person_id,
                'limit': 1,
                'search_after': None
            },
            expected_body={'result': [], 'outcome': {'search_after': []}},
            expected_status=HTTPStatus.OK
        ),
        TestData(
            query_data={
                'person_id': '',
                'limit': 1,
                'search_after': None
            },
            expected_body={'detail': 'Not Found'},
            expected_status=HTTPStatus.NOT_FOUND
        ),
        TestData(
            query_data={
                'person_id': person_id,
                'limit': -1,
                'search_after': None
            },
            expected_body={'detail': [
                {
                    'loc': ['query', 'limit'],
                    'msg': 'ensure this value is greater than or equal to 1',
                    'type': 'value_error.number.not_ge',
                    'ctx': {'limit_value': 1}}
            ]},
            expected_status=HTTPStatus.UNPROCESSABLE_ENTITY
        )
    ]


def generate_incorrect_input_for_search_persons():
    """
    Функция генерирует некорректные входные данные
    для тестирования поиска людей по заданным некорректным параметрам.
    """
    TestData = namedtuple('TestData', ['query_data', 'expected_body', 'expected_status'])
    return [
        TestData(
            query_data={
                'full_name': '@',
                'limit': 1,
                'search_after': None
            },
            expected_body={'result': [], 'outcome': {}},
            expected_status=HTTPStatus.OK
        ),
        TestData(
            query_data={
                'full_name': '',
                'limit': -1,
                'search_after': None
            },
            expected_body={'detail': [
                {
                    'loc': ['query', 'limit'],
                    'msg': 'ensure this value is greater than or equal to 1',
                    'type': 'value_error.number.not_ge',
                    'ctx': {'limit_value': 1}}
            ]},
            expected_status=HTTPStatus.UNPROCESSABLE_ENTITY
        )
    ]


@lru_cache()
def _generate_persons_data(person_count: int) -> Any:
    """
    Функция генерирует тестовые данные людей.

        Args:
            person_count (int): количество генерируемых данных людей.
    """
    test_data = []
    expected_bodies = []

    for index in range(person_count):
        person_id = str(uuid.uuid4())
        person = {
            "_id": person_id,
            'id': person_id,
            'full_name': f'Test person {index}',
            'actor': [str(uuid.uuid4()), str(uuid.uuid4())],
            'director': [str(uuid.uuid4()), str(uuid.uuid4())],
            'writer': [str(uuid.uuid4()), str(uuid.uuid4())],
            'other': [str(uuid.uuid4()), str(uuid.uuid4())],
            'films': [str(uuid.uuid4()), str(uuid.uuid4())]
        }
        test_data.append(person)

        expected_body = person.copy()
        del expected_body['_id']
        expected_body['roles'] = {
            'actor': expected_body.pop('actor'),
            'writer': expected_body.pop('writer'),
            'director': expected_body.pop('director'),
            'other': expected_body.pop('other')
        }
        expected_bodies.append(expected_body)

    return test_data, expected_bodies
