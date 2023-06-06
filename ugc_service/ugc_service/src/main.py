"""Модуль, запускающий `uvicorn` сервер для FastApi-приложения."""

import uvicorn
import asyncio
from aiohttp import ClientSession
import aioredis
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from aiokafka import AIOKafkaProducer

from api.v1.film_rating import film_rating_router
from api.v1.film_review import film_review_router
from api.v1.user_bookmark import user_bookmark_router
from api.v1.events import event_router
from core.config import settings, mongodb_settings, kafka_settings
from ugc_service.src.db import redis
from ugc_service.src.db import kafka, mongodb

from sentry_sdk import init


description = """
### API записи событий и контента пользователей.<br>
"""

init(
    settings.sentry_dsn,
    traces_sample_rate=1.0
)

app = FastAPI(
    title=settings.project_name,
    version=settings.project_version,
    description=description,
    contact={
        "name_1": "Антон",
        "url_1": "https://github.com/mistandok",
        "name_2": "Михаил",
        "url_2": "https://github.com/Mikhail-Kushnerev",
        "name_3": "Евгений",
        "url_3": "https://github.com/ME-progr"
    },
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)

@app.on_event('startup')
async def startup():
    """Метод создает соединения при старте сервера."""

    redis.redis = await aioredis.create_redis_pool(
        (settings.redis_host, settings.redis_port),
        minsize=10,
        maxsize=20,
    )
    setattr(app.state, "api_session", ClientSession(trust_env=True, raise_for_status=True))
    mongodb.mongo_client = AsyncIOMotorClient(
        host=[
            f'{mongodb_settings.mongos1_host}:{mongodb_settings.mongos1_port}',
            f'{mongodb_settings.mongos2_host}:{mongodb_settings.mongos2_port}',
        ],
        serverSelectionTimeoutMS=mongodb_settings.timeout_ms,
    )
    kafka.kafka_producer_client = AIOKafkaProducer(
        bootstrap_servers=kafka_settings.kafka_dsn,
        request_timeout_ms=kafka_settings.timeout_ms,
    )
    await kafka.start_kafka_producer()


@app.on_event('shutdown')
async def shutdown():
    """Метод разрывает соединения при отключении сервера."""

    await kafka.kafka_producer_client.stop()
    mongodb.mongo_client.close()
    redis.redis.close()
    await redis.redis.wait_closed()
    await asyncio.wait((app.state.api_session.close()), timeout=5.0)


app.include_router(film_rating_router, prefix='/ugc/api/v1/film-rating', tags=['rating'])
app.include_router(film_review_router, prefix='/ugc/api/v1/film-review', tags=['review'])
app.include_router(user_bookmark_router, prefix='/ugc/api/v1/user-bookmark', tags=['bookmark'])
app.include_router(event_router, prefix='/ugc/api/v1/event', tags=['event'])


if __name__ == '__main__':

    if settings.debug.lower() == 'true':
        uvicorn.run(
            'main:app',
            host='0.0.0.0',
            port=8101,
        )
