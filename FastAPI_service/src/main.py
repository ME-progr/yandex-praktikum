"""Модуль, запускающий `uvicorn` сервер для FastApi-приложения."""

import uvicorn
import asyncio
from aiohttp import ClientSession
import aioredis
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1.films import films_router
from api.v1.genres import genres_router
from api.v1.persons import persons_router
from core.config import settings
from db import elastic, redis

description = """
### API получения информации для онлайн-кинотеатра.<br>
<br>
Благодаря данному функционалу Вы можете получить<br>
различную информацию в разных форматах о:<br>
&emsp;- фильмах<br>
&emsp;- жанрах<br>
&emsp;- людях, участвующих в создании фильмов<br>
<br>
При этом Вам доступна сортировка и полнотекстовый поиск.<br>
<br>
`Have fun!`<br>
"""

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
    """Метод создает соединения к базам данных при старте сервера."""

    redis.redis = await aioredis.create_redis_pool(
        (settings.redis_host, settings.redis_port),
        minsize=10,
        maxsize=20
    )
    elastic.es = AsyncElasticsearch(hosts=[f'{settings.elastic_host}:{settings.elastic_port}'])
    setattr(app.state, "api_session", ClientSession(trust_env=True, raise_for_status=True))


@app.on_event('shutdown')
async def shutdown():
    """Метод разрывает соединения от баз данных при отключении сервера."""

    redis.redis.close()
    await redis.redis.wait_closed()
    await elastic.es.close()
    await asyncio.wait((app.state.api_session.close()), timeout=5.0)


app.include_router(films_router, prefix='/api/v1/films', tags=['films'])

app.include_router(genres_router, prefix='/api/v1/genres', tags=['genres'])

app.include_router(persons_router, prefix='/api/v1/persons', tags=['persons'])


if __name__ == '__main__':

    if settings.debug.lower() == 'true':
        uvicorn.run(
            'main:app',
            host='0.0.0.0',
            port=8100,
        )
