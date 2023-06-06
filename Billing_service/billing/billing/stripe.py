import stripe
from django.conf import settings

from billing.models import Consumer, Subscribe

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_customer(consumer: Consumer):
    customer = stripe.Customer.create(email=consumer.email)
    consumer.remote_consumer_id = customer.id
    consumer.save()


def create_product(subscribe: Subscribe):
    product = stripe.Product.create(name=subscribe.get_subscribe_type_display())
    price = stripe.Price.create(
        unit_amount=subscribe.price * 100,
        currency="usd",
        recurring={"interval": "month"},
        product=product.id,
    )
    subscribe.payment_id = price.id
    subscribe.save()


def create_subscribe(consumer: Consumer, subscribe: Subscribe):
    checkout_session = stripe.checkout.Session.create(
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


def cancel_subscribe(consumer: Consumer, subscribe: Subscribe):
    subscriptions = stripe.Subscription.list(
        customer=consumer.remote_consumer_id,
        price=subscribe.payment_id,
        status="all",
        expand=["data.default_payment_method"],
    )
    subscription_id = subscriptions["data"][0]["id"]
    stripe.Subscription.delete(subscription_id)
