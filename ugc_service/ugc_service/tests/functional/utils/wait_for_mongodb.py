"""Модуль проверяет состояние Redis."""

import sys

import backoff
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ServerSelectionTimeoutError

from settings import mongodb_settings


@backoff.on_exception(backoff.expo, ServerSelectionTimeoutError)
def wait_mongodb():
    client = AsyncIOMotorClient(
        mongodb_settings.host,
        mongodb_settings.port,
        username=mongodb_settings.username,
        password=mongodb_settings.password,
        serverSelectionTimeoutMS=mongodb_settings.timeout_ms,
    )
    db = client[mongodb_settings.db_name]
    db.command('ping')
    client.close()


if __name__ == '__main__':
    print('waiting for MongoDB...', file=sys.stdout)
    wait_mongodb()
    print('MongoDB was started', file=sys.stdout)
