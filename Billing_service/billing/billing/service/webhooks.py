"""Модуль отвечает за логику обработки вебхуков"""
from abc import ABC, abstractmethod
from enum import Enum

from billing.models import Subscribe, Consumer, Payment
from billing.service.errors import MissWebhookEventRealisation
from billing.service.remote.auth_service import add_role_to_user_by_subscribe, delete_role_from_user_by_subscribe


class WebhookEventType(str, Enum):
    """Названия событий вебхуков."""

    CUSTOMER_SUB_CREATED = 'customer.subscription.created'
    CUSTOMER_SUB_UPDATED = 'customer.subscription.updated'
    CUSTOMER_SUB_DELETED = 'customer.subscription.deleted'

    INVOICE_PAID = 'invoice.paid'


class WebhookEventHandler(ABC):
    """Обработчик событий вебхуков."""
    def __init__(self, data_object: dict):
        self._data_object = data_object

    @abstractmethod
    def execute(self):
        """Запускает обработку различных действий."""


class CustomerSubEventHandler(WebhookEventHandler):
    """Обработчик для действий с подпиской покупателя."""

    def execute(self):
        """Метод обрабатывает события вебхуков, связанные с подписками покупателя."""
        payment_id = self._data_object["plan"]["id"]
        remote_consumer_id = self._data_object["customer"]
        is_sub_active = True if self._data_object["status"] == "active" else False

        subscribe = Subscribe.objects.filter(payment_id=payment_id).first()
        customer = Consumer.objects.filter(remote_consumer_id=remote_consumer_id).first()

        if is_sub_active:
            customer.subscribe.add(subscribe)
            add_role_to_user_by_subscribe(customer.user_id, subscribe.subscribe_type)
        else:
            customer.subscribe.remove(subscribe)
            delete_role_from_user_by_subscribe(customer.user_id, subscribe.subscribe_type)


class InvoicePaidEventHandler(WebhookEventHandler):
    """Обработчик оплаты."""

    def execute(self):
        transaction_id = self._data_object["id"]
        remote_consumer_id = self._data_object["customer"]
        payment_id = self._data_object["lines"]["data"][0]["plan"]["id"]
        amount = self._data_object["lines"]["data"][0]["plan"]["amount"] / 100

        payment = Payment()
        payment.transaction_id = transaction_id
        payment.consumer = Consumer.objects.filter(remote_consumer_id=remote_consumer_id).first()
        payment.subscription = Subscribe.objects.filter(payment_id=payment_id).first()
        payment.amount = amount
        payment.save()


def get_handler_by_event_type(event_type: str, *args, **kwargs) -> WebhookEventHandler:
    """
    Функция получает конкретный обработчик, в зависимости от типа события.

    Args:
        event_type: тип события
        args: позиционные аргументы для обработчика.
        kwargs: именнованные аргументы для обработчика.

    Return:
        WebhookEventHandler
    """
    if event_type in {
        WebhookEventType.CUSTOMER_SUB_CREATED.value,
        WebhookEventType.CUSTOMER_SUB_DELETED.value,
        WebhookEventType.CUSTOMER_SUB_UPDATED.value,
    }:
        return CustomerSubEventHandler(*args, **kwargs)

    if event_type == WebhookEventType.INVOICE_PAID.value:
        return InvoicePaidEventHandler(*args, **kwargs)

    raise MissWebhookEventRealisation(f"Событие {event_type} не обрабатывается сервисом.")
