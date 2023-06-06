"""Модуль описывает реализацию интерфейса для платежной системы stripe."""
from django.conf import settings

import stripe

from billing.models import Consumer, Subscribe
from .interfaces import BasePaymentSystem, PaymentSystemName


class StripePaymentSystem(BasePaymentSystem):
    """Класс-обертка над API-страйпа."""

    __slots__ = ['_client']

    name = PaymentSystemName.STRIPE

    def __init__(self):
        self._client = stripe
        self._client.api_key = settings.STRIPE_SECRET_KEY

    def create_customer(self, consumer: Consumer) -> str:
        remote_customer = self._client.Customer.create(email=consumer.email)
        return remote_customer.id

    def create_product_and_price(self, subscribe: Subscribe) -> tuple[str, str]:
        product = self._client.Product.create(name=subscribe.get_subscribe_type_display())
        price = self._client.Price.create(
            unit_amount=subscribe.price * 100,
            currency=subscribe.currency,
            recurring={"interval": subscribe.interval},
            product=product.id,
        )
        return product.id, price.id

    def create_checkout_session_url(self, consumer: Consumer, subscribe: Subscribe) -> str:
        checkout_session = self._client.checkout.Session.create(
            line_items=[
                {
                    "price": subscribe.payment_id,
                    "quantity": 1,
                },
            ],
            mode="subscription",
            success_url=settings.FRONTEND_SUCCESS_PAYMENT_URL,
            cancel_url=settings.FRONTEND_UNSUCCESS_PAYMENT_URL,
            customer=consumer.remote_consumer_id,
        )
        return checkout_session.url

    def cancel_subscribe(self,  consumer: Consumer, subscribe: Subscribe):
        subscriptions = self._client.Subscription.list(
            customer=consumer.remote_consumer_id,
            price=subscribe.payment_id,
            status="all",
            expand=["data.default_payment_method"],
        )
        subscription_id = subscriptions["data"][0]["id"]
        self._client.Subscription.delete(subscription_id)
