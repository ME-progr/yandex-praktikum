"""Модуль содержит декораторы для работы с кэшем."""

from functools import wraps

from pydantic import BaseModel

from core.config import settings
from .cache import get_cache_by_client
from .exceptions import MissCacheClientInClass


def cache(response_model: BaseModel, expire: int = settings.timeline_of_cache):
    """
    Декоратор, который осуществляет кэширование ответов ручек.

    Args:
        expire: время жизни кэша
        response_model: модель, в которой должен возвращаться ответ
    """
    def decorator(func):
        wraps(func)

        async def wrapper(self, *args, **kwargs):
            try:
                cache_controller = get_cache_by_client(self.cache_client)
            except AttributeError:
                raise MissCacheClientInClass(self.__class__.__name__)
            class_name = self.__class__.__name__
            func_name = func.__name__
            cache_id = cache_controller.make_cache_id_by_template(class_name, func_name, *args, **kwargs)

            cache_response = await cache_controller.get(cache_id)

            if cache_response:
                return response_model(**cache_response)

            func_response = await func(self, *args, **kwargs)
            await cache_controller.put(cache_id, func_response, expire)
            return func_response

        return wrapper

    return decorator
