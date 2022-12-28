import os

from .settings import *

DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ.get("DJANGO_DB_NAME"),
        "USER": os.environ.get("DJANGO_DB_USER"),
        "PASSWORD": os.environ.get("DJANGO_DB_PASSWORD"),
        "HOST": os.environ.get("POSTGRES_HOST"),
        "PORT": os.environ.get("POSTGRES_PORT"),
    }
}

del STATICFILES_DIRS
STATIC_ROOT = BASE_DIR / "static"
STATIC_URL = "/static/"
