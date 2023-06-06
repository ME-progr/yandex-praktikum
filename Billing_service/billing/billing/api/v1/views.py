from http import HTTPStatus

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from billing.serializers import SubscribeSerializer, WebhookSerializer

from billing.service.bearer_auth import generic_bearer_auth, BearerTokenMixin
from billing.service.errors import PaymentError, MissWebhookEventRealisation
from billing.service.payments import PaymentManager
from billing.service.webhooks import get_handler_by_event_type
from billing.service.payment_systems.interfaces import PaymentSystemName


class CreateSubscribe(GenericAPIView, BearerTokenMixin):
    """АПИ для создания подписки пользователя."""

    serializer_class = SubscribeSerializer

    @generic_bearer_auth
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = self.token_payload.sub.user_id
        email = self.token_payload.sub.email
        subscribe_type = serializer.validated_data.get("subscribe_type")

        try:
            payment_manager = PaymentManager(PaymentSystemName.STRIPE)
            url = payment_manager.create_customer_subscribe_payment_link(user_id, email, subscribe_type)
        except PaymentError as e:
            return Response(data=str(e), status=HTTPStatus.BAD_REQUEST)
        except Exception:
            return Response(data='Что-то пошло не так, мы уже решаем проблему', status=HTTPStatus.INTERNAL_SERVER_ERROR)

        return Response(url)


class CancelSubscribe(GenericAPIView, BearerTokenMixin):
    """АПИ для отмены подписки пользователя."""

    serializer_class = SubscribeSerializer

    @generic_bearer_auth
    def delete(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = self.token_payload.sub.user_id
        email = self.token_payload.sub.email
        subscribe_type = serializer.validated_data.get("subscribe_type")

        try:
            payment_manager = PaymentManager(PaymentSystemName.STRIPE)
            is_sub_canceled = payment_manager.cancel_subscribe_for_user(user_id, email, subscribe_type)

            if is_sub_canceled:
                return Response(status=HTTPStatus.NO_CONTENT)

            return Response(data="Пользователя с такой подпиской не существует.", status=HTTPStatus.BAD_REQUEST)
        except Exception:
            return Response(data='Что-то пошло не так, мы уже решаем проблему', status=HTTPStatus.INTERNAL_SERVER_ERROR)


class WebhookAPIView(GenericAPIView):
    """АПИ для обработки событий, которые посылает платежная система."""

    serializer_class = WebhookSerializer

    def post(self, request):
        data = request.data["data"]
        event_type = request.data["type"]
        data_object = data["object"]

        try:
            event_handler = get_handler_by_event_type(event_type, data_object)
            event_handler.execute()
        except MissWebhookEventRealisation:
            pass
        except Exception:
            return Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)

        return Response(status=HTTPStatus.OK)
