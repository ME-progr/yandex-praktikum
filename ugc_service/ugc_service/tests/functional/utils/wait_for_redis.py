"""Модуль проверяет состояние Redis."""

import sys

import backoff
from redis import Redis
from redis.exceptions import ConnectionError

from settings import settings


@backoff.on_exception(backoff.expo, ConnectionError)
def wait_redis():
    redis_client = Redis(host=settings.redis_host, port=settings.redis_port)
    if not redis_client.ping():
        raise ConnectionError
    redis_client.close()


if __name__ == '__main__':
    print('waiting for Redis...', file=sys.stdout)
    wait_redis()
    print('Redis was started', file=sys.stdout)
