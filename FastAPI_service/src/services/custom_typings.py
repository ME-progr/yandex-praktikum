from typing import Union

from elasticsearch import AsyncElasticsearch
from aioredis import Redis

SearchClient = Union[AsyncElasticsearch]

CacheClient = Union[Redis]
