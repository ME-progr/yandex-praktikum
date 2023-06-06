from http import HTTPStatus

import jwt

from rest_framework.request import Request
from rest_framework.response import Response
from django.conf import settings

from .errors import MissBearerAuthorization, MissTokenUserData, MissTokenPayloadAttribute
from .pydantic_models.tokens import AccessTokenPayload
from .utils import is_attribute_in_class


class BearerTokenMixin:
    """Миксин, который добавляет классовый атрибут токена, необходимый для работы."""

    token_payload: AccessTokenPayload = None


def generic_bearer_auth(func):
    """
    Декоратор, который вешается на методы Generic классов.

    P.S.
    Для корректной работы необходимо завести классовый аттрибут token_payload.
    """
    def wrapper(self, request):
        if not is_attribute_in_class(self, "token_payload"):
            raise MissTokenPayloadAttribute(
                "Чтобы использовать декоратор, класссу необходимо добавить миксин BearerTokenMixin."
            )

        try:
            self.token_payload = try_bearer_auth(request)
        except (MissBearerAuthorization, MissTokenUserData) as e:
            return Response(str(e), status=HTTPStatus.UNAUTHORIZED)

        return func(self, request)

    return wrapper


def try_bearer_auth(request: Request) -> AccessTokenPayload:
    """
    Функция пытается проверить, авторизован ли запрос с помощью bearer auth.

    Args:
        request: запрос.

    Raises:
        MissBearerAuthorization
        MissTokenUserData
    """
    try:
        token = request.headers.get("Authorization", "").split(" ")[1]
    except IndexError:
        raise MissBearerAuthorization("Miss token in authorization header")

    token_payload = try_get_token_payload(token)

    if not any((token_payload.sub.user_id, token_payload.sub.email)):
        raise MissTokenUserData("Miss user information for payment.")

    return try_get_token_payload(token)


def try_get_token_payload(encoded_token: str) -> AccessTokenPayload:
    """
    Функция пытается расшифровать токени получить из него информацию.

    Args:
        encoded_token: зашифрованный токен.

    Returns:
        расшифрованый токен.

    Raises:
        MissBearerAuthorization
    """
    try:
        return AccessTokenPayload(**jwt.decode(
            encoded_token,
            settings.JWT_SECRET_KEY.encode("utf-8"),
            algorithms=[settings.JWT_ALGORITHM],
        ))
    except jwt.PyJWTError:
        raise MissBearerAuthorization("Invalid or expired token.")
