"""Различные утилиты для работы с удаленными сервисами."""
from billing.service.errors import MissRemoteServiceSettings


def validate_remote_settings_with_bearer(service_name: str, url: str, token: str):
    """Проверяет факт задания настроек для сервиса."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not all((url, token)):
                raise MissRemoteServiceSettings(f"Не заданы настройки для сервиса {service_name}")
            return func(*args, **kwargs)

        return wrapper

    return decorator
