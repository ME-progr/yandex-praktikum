"""Модуль, запускающий `uvicorn` сервер для FastApi-приложения."""

from contextlib import asynccontextmanager

import uvicorn
from redis.asyncio.client import Redis
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from motor.motor_asyncio import AsyncIOMotorClient

from src.api.v1.user_purchased_films import user_purchased_films_router
from src.core.config import settings, mongodb_settings
from src.db import mongodb
from src.db import redis


description = """
### API для управлния профилями пользователей.<br>
"""


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Фунцкция, производящая действия при старте и при завершении работы сервера."""

    redis.redis = await Redis(host=settings.redis_host, port=settings.redis_port)

    mongodb.mongo_client = AsyncIOMotorClient(
        host=[
            f'{mongodb_settings.mongos1_host}:{mongodb_settings.mongos1_port}',
            f'{mongodb_settings.mongos2_host}:{mongodb_settings.mongos2_port}',
        ],
        serverSelectionTimeoutMS=mongodb_settings.timeout_ms,
        uuidRepresentation='standard',
    )

    yield

    mongodb.mongo_client.close()
    await redis.redis.close()


app = FastAPI(
    lifespan=lifespan,
    title=settings.project_name,
    version=settings.project_version,
    description=description,
    contact={
        'name_1': 'Антон',
        'url_1': 'https://github.com/mistandok',
        'name_2': 'Михаил',
        'url_2': 'https://github.com/Mikhail-Kushnerev',
        'name_3': 'Евгений',
        'url_3': 'https://github.com/ME-progr',
        'name_4': 'Илья',
        'url_4': 'https://github.com/Bexram',
    },
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


app.include_router(user_purchased_films_router, prefix='/profiles/api/v1/user-profile', tags=['user-profile'])


if __name__ == '__main__':

    if settings.debug.lower() == 'true':
        uvicorn.run(
            'main:app',
            host='0.0.0.0',
            port=8102,
        )
