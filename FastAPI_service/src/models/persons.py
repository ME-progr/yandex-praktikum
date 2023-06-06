"""Pydantic-схемы для людей."""

from uuid import UUID

from pydantic import BaseModel

from models.base import UUIDModel


class PersonRoles(BaseModel):
    """Класс для формирования информации о ролях людей."""

    actor: list[UUID]
    writer: list[UUID]
    director: list[UUID]
    other: list[UUID]


class PersonBase(UUIDModel):
    """Класс для представления короткой информации о человеке."""

    full_name: str


class Person(PersonBase):
    """Класс для представления полной информации о человеке."""

    roles: PersonRoles
    films: list[UUID]
