"""Модуль содержащий url для api."""

from django.urls import path, include

urlpatterns = [
    path('v1/', include('billing.api.v1.urls')),
]
