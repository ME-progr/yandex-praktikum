"""Модуль содержит в себе фикстуры для работы с тестовыми данными."""

import pytest_asyncio
from aiohttp.client import ClientSession

from tests.functional.utils.data_work import user_login, signup_user


@pytest_asyncio.fixture(scope='session', autouse=True)
async def prepared_tokens(api_session: ClientSession):
    """
    Фикстура отвечает за подготовительное получение токенов.
    """
    test_login = 'test_user'
    test_email = 'test@email.ru'
    test_pwd = 'test_pwd'
    await signup_user(api_session, test_login, test_email, test_pwd)
    test_access_token, test_refresh_token = await user_login(api_session, test_login, test_pwd)
    yield {
        'test_user': {
            'access_token': test_access_token,
            'refresh_token': test_refresh_token
        }
    }
