import os
from pathlib import Path
from dotenv import load_dotenv
from split_settings.tools import include

load_dotenv()

include(
    "components/database.py",
    "components/apps.py",
    "components/middleware.py",
)

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY", "SECRET_KEY")

DEBUG = os.environ.get("DEBUG", False) == "True"
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOST", "127.0.0.1,localhost").split(",")

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

LANGUAGE_CODE = "ru-RU"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "/static/"

if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = "/media/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

INTERNAL_IPS = [
    "127.0.0.1",
]

JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "best_hwt_secret_key")
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM", "HS256")


STRIPE_PUBLISHABLE_KEY = os.environ.get("STRIPE_PUBLISHABLE_KEY", "pk_test")
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "sk_test")

FRONTEND_SUCCESS_PAYMENT_URL = os.environ.get("FRONTEND_SUCCESS_PAYMENT_URL", "http://localhost:8000/success")
FRONTEND_UNSUCCESS_PAYMENT_URL = os.environ.get("FRONTEND_UNSUCCESS_PAYMENT_URL", "http://localhost:8000/cancel")

AUTH_SERVICE_URL = os.environ.get("AUTH_SERVICE_URL", "localhost:60000")
AUTH_SERVICE_TOKEN = os.environ.get("AUTH_SERVICE_TOKEN", "token")
