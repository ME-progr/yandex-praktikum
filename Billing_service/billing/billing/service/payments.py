"""Модуль содержит Бизнесс логику для работы с платежами."""
from django.core.exceptions import ObjectDoesNotExist

from billing.models import Consumer, Subscribe
from billing.service.errors import PaymentError
from billing.service.payment_systems.factories import get_payment_system_by_name
from billing.service.payment_systems.interfaces import PaymentSystemName


class PaymentManager:
    """Класс-менеджер для работы с подписками."""

    def __init__(self, payment_name: PaymentSystemName):
        self._payment_system = get_payment_system_by_name(payment_name)

    def create_customer_subscribe_payment_link(self, user_id: str, email: str, subscribe_type: str) -> str:
        """
        Функция осуществляет создание покупателя, если его еще нет, и генерирует ссылку для оплаты на подписку.

        Args:
            user_id: идентификатор пользователя.
            email: почта пользователя.
            subscribe_type: тип подписки.

        Returns:
            ссылка на оплату

        Raises:
            PaymentError
        """
        try:
            subscribe = Subscribe.objects.get(subscribe_type=subscribe_type)
        except ObjectDoesNotExist:
            raise PaymentError(f"Подписки {subscribe_type} не существует.")

        customer, created = Consumer.objects.get_or_create(user_id=user_id, email=email)

        if customer.subscribe.filter(subscribe_type=subscribe_type).exists():
            raise PaymentError("У пользователя уже оформлена подписка.")

        return self._payment_system.create_checkout_session_url(consumer=customer, subscribe=subscribe)

    def cancel_subscribe_for_user(self, user_id: str, email: str, subscribe_type: str) -> bool:
        """
        Функция отменяет подписку пользователя.

        Args:
            user_id: идентификатор пользователя.
            email: почта пользователя.
            subscribe_type: тип подписки.

        Returns:
            True - подписка была отменена для пользователя.
            False - пользователя с такой подпиской не существовало.

        """
        customer = Consumer.objects.filter(
            user_id=user_id, email=email, subscribe__subscribe_type=subscribe_type
        ).first()
        if customer:
            subscribe = Subscribe.objects.get(subscribe_type=subscribe_type)
            self._payment_system.cancel_subscribe(customer, subscribe)
            return True

        return False
