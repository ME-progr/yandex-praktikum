"""Модуль, дающий возможность работать с ElasticSearch."""

from elasticsearch import AsyncElasticsearch


es: AsyncElasticsearch | None = None


async def get_elastic() -> AsyncElasticsearch:
    """
    Метод-провайдер, дающий по установленному соединению объект класса AsyncElasticsearch.

    Returns: AsyncElasticsearch-объект

    """
    return es
