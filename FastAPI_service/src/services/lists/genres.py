"""Модуль отвечает за реализацию списочных методов для Жанров."""

from typing import Any

from elasticsearch import ElasticsearchException, AsyncElasticsearch
from pydantic import ValidationError

from models.genres import GenreBase
from models.list_base_models import GenreListResult
from .interfaces import BaseList
from .navigation import Navigation, NavigationType
from .sorting import Sorting


class ElasticsearchGenreList(BaseList):
    """Класс отвечает за отбор списка жанров."""

    def __init__(
            self,
            search_client: AsyncElasticsearch,
            query: dict | None = None,
            sorting: Sorting | None = None,
            navigation: Navigation | None = None,
    ):
        super().__init__(search_client=search_client, query=query, sorting=sorting, navigation=navigation)
        self._init_sorting()
        self._es_body = {
            'query': {
                'match_all': {}
            }
        }

    async def get(self) -> GenreListResult:
        """Метод получает данные по жанрам."""
        if self._navigation and self._navigation.nav_type == NavigationType.SEARCH_AFTER:
            return await self._get_data_for_search_after()

        return GenreListResult(result=[])

    def _init_sorting(self):
        """Метод инициализирует сортировку для списка."""
        if self._sorting:
            if 'id' not in self._sorting.fields_names():
                self._sorting.append_str_field_sorting('id')
            if 'name' in self._sorting.fields_names():
                self._sorting.update_field_name('name', 'name.raw')

        self._set_default_sorting()

    def _set_default_sorting(self):
        """Метод задает сортировку по умолчанию."""
        self._sorting = Sorting()
        self._sorting.append_str_field_sorting('name.raw')
        self._sorting.append_str_field_sorting('id')

    async def _get_data_for_search_after(self) -> GenreListResult:
        """Получаем данные для навигации search_after"""
        self._set_navigation_to_es_body()
        self._set_sort_to_es_body()
        hits = await self._get_elastic_hits()
        return self._make_answer_from_es_hits(hits)

    def _set_navigation_to_es_body(self):
        """Метод устанавливает параметры навигации по запросу."""
        if self._navigation.search_after:
            self._es_body.update({'search_after': self._navigation.search_after})

        self._es_body.update({'size': self._navigation.limit})

    def _set_sort_to_es_body(self):
        """Метод формирует параметры сортировки для выборки из `ElasticSearch`"""
        sort = self._get_sorting_body()
        self._es_body.update(sort)

    async def _get_elastic_hits(self) -> list[dict]:
        """Метод возвращает совпадения из elasticsearch"""
        try:
            es_result = await self._search_client.search(
                body=self._es_body,
                index='genres',
            )
        except ElasticsearchException:
            return []

        return es_result.get('hits', {}).get('hits', [])

    @staticmethod
    def _make_answer_from_es_hits(hits: list[dict[str, Any]]) -> GenreListResult:
        """
        Метод формирует итоговый результат по жанрам, попавшим в выборку.

        Args:
            hits (list[dict[str, Any]]): выборка жанров из `ElasticSearch`

        Returns:
            GenreListResult
        """
        last_sort, genres = [], []

        try:
            for row in hits:
                genres.append(GenreBase(**row.get('_source')))
                last_sort = row.get('sort')
        except ValidationError:
            return GenreListResult(result=[], outcome={})

        return GenreListResult(result=genres, outcome={'search_after': last_sort})
