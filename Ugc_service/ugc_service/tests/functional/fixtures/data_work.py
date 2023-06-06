"""Модуль содержит в себе фикстуры для работы с тестовыми данными."""

import pytest_asyncio
from aioredis import Redis

from utils.data_work import cleanup_cache_storage


@pytest_asyncio.fixture(scope='session', autouse=True)
async def data_work(redis_client: Redis):
    """
    Фикстура отвечает за работу с данными в хранилищах
    в начале сессиии и перед завершением сессии.
    Перед завершением сессии происходит
    удаление тестовых данных и кэша из используемых хранилищ.
    """
    yield
    await cleanup_cache_storage(redis_client)


@pytest_asyncio.fixture(scope='session', autouse=True)
async def prepared_tokens():
    """
    Фикстура отвечает за подготовительное получение токенов.
    """

    admin_access_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjc5NzM1ODI5LCJqdGkiOiJiODRkZDA2Zi03MDMxLTRmZTQtOTA4OC1lZDIxMzcwYjkyNjgiLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjp7InVzZXJfaWQiOiJkZmM3Y2I3YS0yNTlhLTQ2MDktYmU0NS0wODdkMzA5ZDU0NWMiLCJ1c2VyX3JvbGVzIjpbImFkbWluIl0sInVzZXJfYWdlbnQiOiJtb2JpbGUiLCJyZWZyZXNoX2p0aSI6IjljZDdhZWVlLWMzOTMtNGQ3NC1iMGU2LWUyZTZiMDg0ZWE1MCJ9LCJuYmYiOjE2Nzk3MzU4MjksImV4cCI6MTY3OTc0MzAyOX0.EmLwK_Riuhf03iOkeDhpXWk8CFcZtfZ_tCnRRjsd9Nw'
    user_access_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjc5NzM1ODY4LCJqdGkiOiIwMmJkNDdmMy1iY2NmLTRkY2ItYWY1OS1jODhmYTI3M2JjYTMiLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjp7InVzZXJfaWQiOiIwNmY1YmRkZS00ZjUwLTQ5NTYtYTQ5ZC1hZTA3Mzc5ODA5YjYiLCJ1c2VyX3JvbGVzIjpbInVzZXIiXSwidXNlcl9hZ2VudCI6Im1vYmlsZSIsInJlZnJlc2hfanRpIjoiMWNlZWYwZmMtYjBmZi00MGUyLTg1N2QtOTk1OWRlNjA0ZDFlIn0sIm5iZiI6MTY3OTczNTg2OCwiZXhwIjoxNjc5NzQzMDY4fQ.y8u7zzHHNl-jxkFkhObe63Lqe9Hv0Hn2WR15Q-fX6t4'
    yield {'admin_access_token': admin_access_token, 'user_access_token': user_access_token}
