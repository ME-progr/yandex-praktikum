"""Модуль содержит методы и классы для генерации объектов списковых методов."""

from core.config import SourceData
from .exceptions import MissListRealisation
from .films import ElasticsearchFilmsList
from .genres import ElasticsearchGenreList
from .interfaces import BaseList
from .persons import ElasticsearchPersonsList


class ListFactory:
    """Клас помогает определить конкретную реализацию для спискового метода."""

    @staticmethod
    def get_list_searcher_by_target(target: SourceData, *args, **kwargs) -> BaseList:
        """Метод предоставляет инстанс спискового метода на основе целевого источника данных."""

        mapping = {
            SourceData.ES_GENRES: ElasticsearchGenreList,
            SourceData.ES_PERSONS: ElasticsearchPersonsList,
            SourceData.ES_MOVIES: ElasticsearchFilmsList,
        }

        try:
            return mapping[target](*args, **kwargs)
        except KeyError:
            raise MissListRealisation(target.value)
