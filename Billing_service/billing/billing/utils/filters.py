"""Модуль фильтров для админки."""

from string import ascii_lowercase
from django.contrib import admin

from billing.utils.constants import Price


class FilmworkFilterAdmin(admin.SimpleListFilter):
    """Класс-фильтр по первой букве фильма"""

    title = 'Алфавит'
    parameter_name = 'фильмы'

    def lookups(self, request, model_admin):
        """Метод формирует доступный алфавит для поиска"""
        return [(letter, letter) for letter in ascii_lowercase]

    def queryset(self, request, queryset):
        """Метод выдаёт результат по фильтру"""
        if self.value():
            queryset = queryset.filter(title__startswith=self.value())
        return queryset


class SubscribeFilterAdmin(admin.SimpleListFilter):
    """Класс-фильтр по цене подписки"""

    title = 'Цена'
    parameter_name = 'подписки'

    def lookups(self, request, model_admin):
        """Метод формирует доступные ценовые диапазоны"""
        return [(price.value, price.value) for price in Price]

    def queryset(self, request, queryset):
        """Метод выдаёт результат по фильтру"""
        if self.value():
            min_, max_ = self.value().split('-')
            queryset = queryset.filter(price__gte=min_, price__lte=max_)
        return queryset
