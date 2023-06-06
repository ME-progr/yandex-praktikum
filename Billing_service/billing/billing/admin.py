"""Модуль интерфейса админки"""

from django.contrib import admin
from .models import Consumer, Payment, Subscribe, Filmwork, FilmworkSubscribe
from .utils.filters import SubscribeFilterAdmin, FilmworkFilterAdmin


class SubscribeFilmworkInline(admin.TabularInline):
    """Интерфейс подписок у кинопроизведения в админке"""
    model = FilmworkSubscribe
    autocomplete_fields = ('subscribe',)


class ConsumerSubscribeInline(admin.TabularInline):
    """Интерфейс подписок у покупателя в админке"""
    model = Consumer.subscribe.through
    autocomplete_fields = ('subscribe',)


@admin.register(Consumer)
class ConsumerAdmin(admin.ModelAdmin):
    """Интерфейс покупателя в админке"""
    inlines = (ConsumerSubscribeInline,)
    list_display = ('__str__', 'user_id', 'remote_consumer_id')
    search_fields = ('user_id',)
    list_per_page = 20


@admin.register(Payment)
class PaymentsAdmin(admin.ModelAdmin):
    """Интерфейс платежа в админке"""
    list_display = ('__str__', 'amount', 'created_at')


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    """Интерфейс подписки в админке"""
    search_fields = ('subscribe_type',)
    list_filter = (SubscribeFilterAdmin,)
    list_display = ('subscribe_type', 'price', 'description')
    ordering = ('price',)
    list_per_page = 20


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    """Интерфейс кинопроизведения в админке"""
    inlines = (SubscribeFilmworkInline,)
    list_filter = (FilmworkFilterAdmin,)
    list_display = ('title', 'modified_subscribe_date')
    search_fields = ("title__startswith",)
    ordering = ('title',)
    list_per_page = 20
