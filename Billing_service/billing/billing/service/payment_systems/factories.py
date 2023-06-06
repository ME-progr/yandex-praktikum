from .interfaces import BasePaymentSystem, PaymentSystemName
from .stripe_payment import StripePaymentSystem
from ..errors import MissPaymentSystemRealisation


def get_payment_system_by_name(name: PaymentSystemName, *args, **kwargs) -> BasePaymentSystem:
    """
    Функция получает платежную систему по ее наименованию.

    Args:
        name: наименование платежной системы.
        args: позиционные аргументы.
        kwargs: именованные аргументы.
    """
    for subclass in BasePaymentSystem.__subclasses__():
        if subclass.name == name:
            return subclass(*args, **kwargs)

    raise MissPaymentSystemRealisation(f"Отсутствует реализация для платежной системы {name}")
