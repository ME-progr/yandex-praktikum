"""Модуль содержит команду для создания подписок."""

from django.core.management.base import BaseCommand
from django.db.models.signals import post_save

from billing.models import Subscribe
from billing.utils.constants import factory


class Command(BaseCommand):
    """
    Класс предназначен для реализации команды manage.py по созданию подписок, если они отсутствуют.
    """

    def handle(self, *args, **options):
        """
        Метод создает базовые подписки.

        Args:
            args: позиционные аргументы.
            options: именнованные аргументы.
        """

        for sub_type in Subscribe.SubscribeType:

            item = Subscribe.objects.filter(subscribe_type=sub_type).exists()

            if item:
                continue

            instance = Subscribe(**factory(sub_type).to_dict())
            instance.save()
