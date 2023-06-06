"""Модуль проверяет состояине Elasticsearch."""

import sys

import backoff
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError, NotFoundError

from settings import settings


@backoff.on_exception(backoff.expo, ConnectionError)
def wait_es():
    es_client = Elasticsearch(
        hosts=f'{settings.elastic_host}:{settings.elastic_port}',
        validate_cert=False,
        use_ssl=False,
    )

    if not es_client.ping():
        raise ConnectionError

    wait_es_indexes(es_client)
    es_client.close()


@backoff.on_exception(backoff.expo, NotFoundError)
def wait_es_indexes(es_client):
    for index in settings.elastic_index:
        if not es_client.indices.exists(index=index.value):
            raise NotFoundError


if __name__ == '__main__':
    print('waiting for Elasticsearch...', file=sys.stdout)
    wait_es()
    print('Elasticsearch was started', file=sys.stdout)
