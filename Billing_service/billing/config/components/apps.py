from django.conf import settings

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "billing.apps.BillingConfig",
    "drf_yasg",
]
if settings.DEBUG:
    INSTALLED_APPS += []
