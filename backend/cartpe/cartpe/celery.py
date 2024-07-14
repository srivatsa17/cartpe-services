import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cartpe.settings")

app = Celery("cartpe", broker_connection_retry_on_startup=False)

# Load the celery configuration from Django settings.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Discover asynchronous tasks in Django app modules.
app.autodiscover_tasks()
