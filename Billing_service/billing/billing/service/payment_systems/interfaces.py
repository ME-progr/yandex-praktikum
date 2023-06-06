"""Модуль содержит интерфейсы для платежных систем."""
from abc import ABC, abstractmethod
from enum import Enum

from billing.models import Consumer, Subscribe


class PaymentSystemName(str, Enum):
    """Наименования платежных систем"""

    BASE = 'base'
    STRIPE = 'stripe'


class BasePaymentSystem(ABC):
    """Базовый класс для платежных систем."""

    name = PaymentSystemName.BASE

    @abstractmethod
    def create_customer(self, consumer: Consumer) -> str:
        """
        Создает в платежной системе клиента.

        Args:
            consumer: наш локальный клиент.

        Returns:
            идентификатор клиента в платежной системе.
        """

    @abstractmethod
    def create_product_and_price(self, subscribe: Subscribe) -> tuple[str, str]:
        """
        Создает продукт и цену для продукта в платежной системе.

        Args:
            subscribe: наш локальный тип подписки

        Returns:
            tuple(product_id, price_id)
        """

    @abstractmethod
    def create_checkout_session_url(self, consumer: Consumer, subscribe: Subscribe) -> str:
        """
        Создает ссылку, по которой необходимо перейти и совершить платеж

        Args:
            consumer: локальный клиент.
            subscribe: локальный тип подписки, которую необходимо оплатить.

        Returns:
            ссылка для оплаты.
        """

    @abstractmethod
    def cancel_subscribe(self,  consumer: Consumer, subscribe: Subscribe):
        """
        Метод отменяет подписку для клиента.

        Args:
            consumer: локальный клиент.
            subscribe: локальный тип подписки, которую необходимо отменить.
        """
