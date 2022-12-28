import os

from celery import Celery


celery_app = Celery("braniac")
celery_app.config_from_object("django.conf:settings", namespace="CELERY")
celery_app.autodiscover_tasks()
