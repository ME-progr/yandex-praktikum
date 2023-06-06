"""Модуль содержит модели для работы с токенами и аутентификацией по токенам."""

from pydantic import BaseModel


class AccessTokenSub(BaseModel):
    """Класс описывает sub-модель access-token."""

    user_id: str
    email: str
    refresh_jti: str
    user_roles: list[str] | None = None
    user_agent: str | None = None


class AccessTokenPayload(BaseModel):
    """Класс описывает модель access-token."""

    fresh: bool
    iat: int
    jti: str
    type: str
    sub: AccessTokenSub
    nbf: int
    exp: int | None
