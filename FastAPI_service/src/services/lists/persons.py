"""Модуль содержит пример работы с сущностями, описанными в модуле lists."""

from typing import Any

from elasticsearch import AsyncElasticsearch, ElasticsearchException
from pydantic import ValidationError

from models.list_base_models import PersonListResult
from services.persons_helpers import adapt_elastic_row_to_person
from .interfaces import BaseList
from .navigation import Navigation, NavigationType
from .sorting import Sorting


class ElasticsearchPersonsList(BaseList):
    """Класс по составлению выборки информации о людях из `ElasticSearch` по заданным параметрам."""

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

    async def get(self) -> PersonListResult:
        """Получение данных"""
        self._create_sort()

        if self._navigation.nav_type == NavigationType.SEARCH_AFTER:
            return await self._get_search_after_result()

        return PersonListResult(result=[], outcome={})

    def _init_sorting(self):
        """Инициализация сортировки, если она не была задана. Нужно для search_after."""
        if self._sorting:
            self._correct_existed_sorting()
            return None
        self._set_default_sorting()

    def _correct_existed_sorting(self):
        """Метод корректирует заданную сортировку."""
        subfields = ['full_name']
        for subfield in subfields:
            if subfield in self._sorting.fields_names():
                self._sorting.update_field_name(
                    subfield,
                    f'{subfield}.raw'
                )

        mandatory_fields = ['full_name.raw']

        for mandatory_field in mandatory_fields:
            if mandatory_field not in self._sorting.fields_names():
                self._sorting.append_str_field_sorting(mandatory_field)

    def _set_default_sorting(self):
        """Установка сортировки по умолчанию"""
        self._sorting = Sorting()
        self._sorting.append_str_field_sorting('full_name.raw')
        self._sorting.append_str_field_sorting('id')

    async def _get_search_after_result(self) -> PersonListResult:
        """Метод для получения результата по параметру `search_after`."""
        self._set_navigation_to_es_body()
        self._set_query_to_es_body()

        es_result = await self._get_response_from_elastic()
        return await self._make_answer_from_es_results(es_result)

    def _set_navigation_to_es_body(self):
        """Метод устанавливает параметры навигации к запросу."""
        if self._navigation.search_after:
            self._es_body.update({'search_after': self._navigation.search_after})

        self._es_body.update({'size': self._navigation.limit})

    def _create_sort(self):
        """Метод формирует параметры сортировки для выборки из `ElasticSearch`."""
        sort = self._get_sorting_body()
        self._es_body.update(sort)

    async def _get_response_from_elastic(self) -> dict:
        """Метод для получения выборки из `ElasticSearch` по сформированному запросу."""
        try:
            return await self._search_client.search(
                body=self._es_body,
                index='persons',
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
        elif 'full_name' in self._query:
            self._es_body.update(
                {
                    'query': {
                        'match': {
                            'full_name': self._query.get('full_name')
                        }
                    }
                }
            )

    async def _make_answer_from_es_results(self, es_result: dict[str, Any]) -> PersonListResult:
        """
        Метод, формирующий итоговый результат по информацци о людях, попавшие в выборку
        Args:
            es_result (dict[str, Any]): выборка людей из `ElasticSearch`

        Returns:
            Person
        """
        persons = es_result.get('hits', {}).get('hits', [])
        if not persons:
            return PersonListResult(result=[], outcome={})

        last_sort = persons[-1].get('sort')

        try:
            persons = [adapt_elastic_row_to_person(row.get('_source')) for row in persons]
        except ValidationError:
            return PersonListResult(result=[], outcome={})
        return PersonListResult(result=persons, outcome={'search_after': last_sort})
