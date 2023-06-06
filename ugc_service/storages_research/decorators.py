"""Модуль содержит в себе различные декораторы для тестирования."""
from functools import wraps


def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result

    return wrapper
