"""Модуль содержит различные миксины для работы."""


class MongoDBTargetMixin:
    """Миксин, позволяющий задать название целевой базы и коллекции для MongoDB."""

    db_name: str | None = None
    collection_name: str | None = None
