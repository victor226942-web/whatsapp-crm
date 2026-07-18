import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "whatsapp_crm.settings")

app = Celery("whatsapp_crm")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
