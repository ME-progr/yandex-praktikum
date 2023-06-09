"""Модуль для настройки конфигурации URL."""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('movie-admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('api/', include('movies.api.urls')),
]
