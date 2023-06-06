"""Pydantic-схемы для разрешений пользователей."""

from pydantic import BaseModel


class PermissionsResponse(BaseModel):
    """Класс для формирования информации о разрешениях людей."""

    admin: bool
    write: bool
    read: bool
