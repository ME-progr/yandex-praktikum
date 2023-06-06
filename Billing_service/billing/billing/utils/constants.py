"""Модуль константных значений"""

from dataclasses import dataclass, asdict
from decimal import Decimal
from enum import Enum

from billing.models import Subscribe
from config.settings import BASE_DIR


class Price(str, Enum):
    """Класс описывает денежный интервал"""
    STANDART = '199-259'
    DELUXE = '399-799'
    ULTIMATE = '1_500-3_200'


@dataclass
class SubscribeBase:
    """Базовый класс описания значений у подписок"""
    subscribe_type: str | None = None
    description: str | None = None

    def __post_init__(self):
        """Инициализирующий метод. Заполняет описание подписки по его типу."""

        manual_path = BASE_DIR / 'docs' / 'manual'

        with open(
                manual_path / f'{self.subscribe_type}.txt',
                mode='r',
                encoding='utf-8',
                newline=''
        ) as f:
            description = f.read()

        self.description = description

    def to_dict(self):
        """Метод конвертирует объект в словарь."""
        return asdict(self)


@dataclass(slots=True)
class SubscribeCinema(SubscribeBase):
    """Класс описывает подписку `Наш кинотеатр`."""
    subscribe_type: str = Subscribe.SubscribeType.SUBSCRIBER
    price: Decimal = 199
    currency: str = Subscribe.CurrencyType.USD
    interval: str = Subscribe.IntervalType.MONTH


@dataclass(slots=True)
class SubscribeAmediateka(SubscribeBase):
    """Класс описывает подписку `Амедиатека`."""
    subscribe_type: str = Subscribe.SubscribeType.AMEDIATEKA
    price: Decimal = 259
    currency: str = Subscribe.CurrencyType.USD
    interval: str = Subscribe.IntervalType.MONTH


def factory(prefix):
    subscribe_value = {
        Subscribe.SubscribeType.SUBSCRIBER: SubscribeCinema,
        Subscribe.SubscribeType.AMEDIATEKA: SubscribeAmediateka
    }
    return subscribe_value.get(prefix)(prefix)
