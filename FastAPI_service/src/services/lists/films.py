"""Модуль содержит пример работы с сущностями, описанными в модуле lists."""

import logging
from typing import Any

from elasticsearch import AsyncElasticsearch, ElasticsearchException
from pydantic import ValidationError

from models.films import FilmBase
from models.list_base_models import FilmListResult
from .interfaces import BaseList
from .navigation import Navigation, NavigationType
from .sorting import Sorting


class ElasticsearchFilmsList(BaseList):
    """Класс по составлению выборки фильмов из `ElasticSearch` по заданным параметрам."""

    def __init__(
            self,
            es_client: AsyncElasticsearch,
            query: dict | None = None,
            sorting: Sorting | None = None,
            navigation: Navigation | None = None,
    ):
        super().__init__(es_client, query, sorting, navigation)
        self._init_sorting()
        self._es_body = {}

    async def get(self) -> FilmListResult:
        """Получение данных"""
        self._create_sort()

        if self._navigation.nav_type == NavigationType.SEARCH_AFTER:
            return await self._get_search_after_result()

        return FilmListResult(result=[], outcome={})

    def _init_sorting(self):
        """Инициализация сортировки, если она не была задана. Нужно для search_after."""
        if self._sorting:
            self._correct_existed_sorting()
            return None
        self._set_default_sorting()

    def _correct_existed_sorting(self):
        """Метод корректирует заданную сортировку."""
        subfields = ['title']
        for subfield in subfields:
            if subfield in self._sorting.fields_names():
                self._sorting.update_field_name(
                    subfield,
                    f'{subfield}.raw'
                )

        mandatory_fields = ['title.raw']

        for mandatory_field in mandatory_fields:
            if mandatory_field not in self._sorting.fields_names():
                self._sorting.append_str_field_sorting(mandatory_field)

    def _set_default_sorting(self):
        """Установка сортировки по умолчанию"""
        self._sorting = Sorting()
        self._sorting.append_str_field_sorting('-imdb_rating')
        self._sorting.append_str_field_sorting('title.raw')

    async def _get_search_after_result(self) -> FilmListResult:
        """Метод для получения результата по параметру `search_after`."""
        self._set_navigation_to_es_body()
        self._set_query_to_es_body()

        es_result = await self._get_response_from_elastic()
        return await self._make_answer_from_es_results(es_result)

    def _set_navigation_to_es_body(self):
        """Метод, устанавливающий параметры навигации к запросу."""
        if self._navigation.search_after:
            self._es_body.update({'search_after': self._navigation.search_after})

        self._es_body.update({'size': self._navigation.limit})

    def _create_sort(self):
        """Метод, формирующий параметры сортировки для выборки из `ElasticSearch`"""
        sort = self._get_sorting_body()
        self._es_body.update(sort)

    async def _get_response_from_elastic(self) -> dict:
        """Метод для получения выборки из `ElasticSearch` по сформированному запросу."""
        try:
            return await self._search_client.search(
                body=self._es_body,
                index='movies',
            )
        except ElasticsearchException:
            return {}

    def _set_query_to_es_body(self):
        """Метод формирует запрос к `ElasticSearch`."""
        if not self._query:
            self._es_body.update(
                {
                    'query': {
                        'match_all': {}
                    }
                }
            )
        elif 'genres' in self._query:
            self._es_body.update(
                {
                    'query': {
                        'nested': {
                            'path': 'genres',
                            'query': {
                                'bool': {
                                    'must': [
                                        {'terms': {'genres.id': self._query.get('genres')}}
                                    ]
                                }
                            }
                        },
                    }
                }
            )
        elif 'title' in self._query:
            self._es_body.update(
                {
                    'query': {
                        'match': {
                            'title': self._query.get('title')
                        }
                    }
                }
            )
        elif 'persons' in self._query:
            self._es_body.update(
                {
                    'query': {
                        'terms': {
                            'persons': self._query.get('persons')
                        }
                    }
                }
            )

    async def _make_answer_from_es_results(self, es_result: dict[str, Any]) -> FilmListResult:
        """
        Метод, формирующий итоговый результат по фильмам, попавшие в выборку
        Args:
            es_result (dict[str, Any]): выборка фильмов из `ElasticSearch`

        Returns:
            FilmListResult
        """
        results = es_result.get('hits', {}).get('hits', [])
        last_sort = []
        movies = []

        try:
            for result in results:
                film = FilmBase(**result.get('_source'))
                movies.append(film)
                last_sort = result.get('sort')
        except ValidationError:
            logging.error('not validate values')
            return FilmListResult(result=[], outcome={})
        return FilmListResult(result=movies, outcome={'search_after': last_sort})
